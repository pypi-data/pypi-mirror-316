import itertools
from collections.abc import Callable
from datetime import date, timedelta
from time import time
from typing import Dict, List, Optional, Union

from . import _request_tools as rt
from . import _token
from ._misc import flatten, init_logging, make_date, print_feedback
from .types import (Assignment, Course, Exercise, InsightsAssignment,
                    InsightsQuestion, Question, Result)

DEFAULT_N_THREADS = 8
INTERMEDIATE_SAVE = 300


class ANSApi(object):

    URL = "https://ans.app/api/v2/"
    SAVE_INTERVALL = 10

    def __init__(self, n_threads: int = DEFAULT_N_THREADS):
        self._save_callback_fnc = None
        self.__auth_header = None
        self._n_threads = 1
        self.feedback_queue = None
        self.cache = rt.Cache()

        self.n_threads = n_threads
        self.init_token()
        init_logging()

    @property
    def n_threads(self) -> int:
        return self._n_threads

    @n_threads.setter
    def n_threads(self, val: int):
        if val < 1:
            val = 1
        self._n_threads = val

    def init_token(self):
        try:
            token_str = _token.read()
        except RuntimeError:
            self.__auth_header = None
            return
        self.__auth_header = {"Authorization":
                              "Token token={}".format(token_str)}

    @property
    def has_token(self):
        return self.__auth_header is not None

    def _check_token(self):
        if self.__auth_header is None:
            raise RuntimeError(_token.NO_TOKEN_ERROR_MSG)

    @staticmethod
    def make_url(what, query_txt="",
                 page: Optional[int] = None,
                 items: Optional[int] = 100) -> str:
        """if getting multiple items (see ANS API doc) define items and page
        """
        if isinstance(items, int) and isinstance(page, int):
            what = what + f"?items={items}&page={page}"

        url = ANSApi.URL + what
        if len(query_txt):
            if url.find("?") > 0:
                # question separator already in url -> use &
                sep = "&"
            else:
                sep = "?"
            url = url + sep + "query=" + query_txt

        return url

    def save_callback_fnc(self, fnc):
        self._save_callback_fnc = fnc

    def _save_intermediate(self):
        # intermediate save, if save_callback_fnc is defined
        if isinstance(self._save_callback_fnc, Callable):
            self._save_callback_fnc()

    def get(self, url, ignore_http_error=False) -> Union[Dict, None, List[Dict]]:
        """Returns the requested response or None

        Function delays if required.
        """
        self._check_token()
        rtn = rt.wait_request_json(url, headers=self.__auth_header,
                                   ignore_http_error=ignore_http_error)
        if rtn is not None:
            self.cache.add(url, rtn)
        return rtn

    def get_multiple_pages(self, what, query_txt: str = "",
                           items: int = 100,
                           start_page_counter: int = 1) -> List[Dict]:
        """Returns the result of a multiple pages request
            - all pages (from start cnt) of a multiple item request

        Might return [], if nothing received

        Sequentially calls all pages and quits if last page is received.
        Function delays if required

        Note: Use make_url and get(url), if you need a particular page
        """

        self._check_token()
        rtn_lists = []
        page_cnt = start_page_counter - 1

        while True:
            page_cnt = page_cnt + 1
            url = ANSApi.make_url(what=what, items=items, page=page_cnt,
                                  query_txt=query_txt)

            new_list = self.cache.get(url)
            if new_list is None:
                # retrieve online
                new_list = self.get(url)

            if new_list is None or len(new_list) == 0:
                break  # end request loop, because nothing received
            else:
                if new_list in rtn_lists:
                    break  # end request loop, because new list has already been received

                rtn_lists.append(new_list)
                if len(new_list) < items:
                    break  # end request loop, because less items than requested

        return flatten(rtn_lists)

    def find_assignments(self,
                         start_date: Union[str, date],
                         end_date: Union[str, date]) -> List[Assignment]:
        oneday = timedelta(days=1)
        if not isinstance(start_date, date):
            start_date = make_date(start_date)
        if not isinstance(end_date, date):
            end_date = make_date(end_date)

        period = f"start_at>'{start_date - oneday}' start_at<'{end_date + oneday}'"

        self._feedback(f"retrieving assignments: {period}")

        assignments = self.get_multiple_pages(what="search/assignments",
                                              query_txt=period)
        self._feedback("  found {} assignments".format(len(assignments)))
        return [Assignment(d) for d in assignments]

    def download_course_info(self, assignments: Union[Assignment, List[Assignment]],
                             feedback=True) -> None:
        if isinstance(assignments, Assignment):
            assignments = [assignments]  # force list
        # make urls
        urls = []
        for ass in assignments:
            cid = ass.dict["course_id"]  # type: ignore
            urls.append(ANSApi.make_url(what=f"courses/{cid}"))

        responses = self._get_multiprocessing(urls)

        fcnt = 0
        l = len(assignments)
        for ass, rsp in zip(assignments, responses):
            ass.course = Course(rsp)
            if feedback:
                fcnt = fcnt + 1
                self._feedback(f" ({fcnt}/{l}) {ass.formated_label()}")

    def download_results(self, assignments: Union[Assignment, List[Assignment]],
                         force_update: bool = False) -> bool:

        # downloads results and writes it to assignment
        if isinstance(assignments, Assignment):
            assignments = [assignments]  # force list

        if not force_update:
            # filter list (only those without responses)
            assignment_list = [
                ass for ass in assignments if ass.results_undefined]
        else:
            assignment_list = assignments

        if len(assignment_list) == 0:
            return False

        # what list
        what_list = []
        feedback_list = []
        for ass in assignment_list:
            what_list.append(f"assignments/{ass.id}/results")
            feedback_list.append("[results] {}".format(ass.dict["name"]))

        chunck_size = 100
        i = 0
        while True:
            j = i + chunck_size
            responses = self._get_multiprocessing_multipages(
                what_list=what_list[i:j],
                items=100,
                feedback_list=feedback_list[i:j])

            for ass, rsp in zip(assignment_list[i:j], responses):
                ass.results = [Result(obj) for obj in rsp]
            i = j
            if i > len(assignment_list)-1:
                break
            self._save_intermediate()

        return True

    def download_assignment_insights(self, assignments: Union[Assignment, List[Assignment]],
                                     force_update: bool = False, feedback=True) -> bool:

        if isinstance(assignments, Assignment):
            assignments = [assignments]  # force list

        if not force_update:
            # filter list (only those without responses)
            assignment_list = [
                ass for ass in assignments if ass.insights is None]
        else:
            assignment_list = assignments

        # make urls
        urls = []
        feedback = []
        fcnt = 0
        n_ass = len(assignment_list)
        if n_ass == 0:
            return False

        for ass in assignment_list:
            fcnt = fcnt + 1
            urls.append(ANSApi.make_url(what=f"insights/assignments/{ass.id}"))
            feedback.append(f"[assignment insights] {fcnt}/{n_ass}")

        responses = self._get_multiprocessing(urls, ignore_http_error=True,
                                              feedback_list=feedback)

        for ass, rsp in zip(assignments, responses):
            ass.insights = InsightsAssignment(rsp)

        return True

    def download_exercises_and_questions(self,
                                         assignments: Union[Assignment, List[Assignment]],
                                         force_update: bool = False) -> bool:
        # downloads results and writes it to assignment
        if isinstance(assignments, Assignment):
            assignments = [assignments]  # force list

        if not force_update:
            # filter list (only those without responses)
            assignment_list = [
                ass for ass in assignments if len(ass.exercises) == 0]
        else:
            assignment_list = assignments


        last_save = time()
        n_ass = len(assignment_list)
        if n_ass == 0:
            return False

        for c, ass in enumerate(assignment_list):
            r = self.get_multiple_pages(what=f"assignments/{ass.id}/exercises")
            if len(r):
                self._feedback(
                    f"[{len(r)} exercises] {c}/{n_ass}   {ass.dict['name']}")
                ass.exercises = [Exercise(obj) for obj in r]
                self._download_questions(ass.exercises)  # multi thread
            if time() - last_save > ANSApi.SAVE_INTERVALL:
                self._save_intermediate()
                last_save = time()

        return True

    def _download_questions(self, exercises: Union[Exercise, List[Exercise]]):
        if isinstance(exercises, Exercise):
            exercises = [exercises]  # force list
        urls = []
        for obj in exercises:
            urls.append(ANSApi.make_url(
                what=f"exercises/{obj.id}/questions",
                items=50, page=1))  # should be enough questions per exercise
        responses = self._get_multiprocessing(urls)
        for obj, rsp in zip(exercises, responses):
            obj.questions = [Question(obj) for obj in rsp]

    def download_question_insights(self,
                                   assignments: Union[Assignment, List[Assignment]],
                                   force_update: bool = False) -> bool:
        if isinstance(assignments, Assignment):
            assignments = [assignments]  # force list

        # make urls
        urls = []
        questions = []
        for quest in assignments:
            for ex in quest.exercises:
                for quest in ex.questions:
                    if quest.insights_undefined or force_update:
                        urls.append(ANSApi.make_url(
                            what=f"insights/questions/{quest.id}"))
                        questions.append(quest)

        n_quest = len(questions)
        if n_quest ==0:
            return False

        feedback_lst = [
            f"[question insights] {cnt+1}/{n_quest}" for cnt in range(n_quest)]
        responses = self._get_multiprocessing(urls, ignore_http_error=False,
                                              feedback_list=feedback_lst)  # type: ignore
        for quest, rsp in zip(questions, responses):
            quest.insights = InsightsQuestion(rsp)

        return True

    def download_submissions_and_student_info(self,
                                              assignments: Union[Assignment, List[Assignment]],
                                              force_update: bool = False) -> bool:
        # downloads submissions and student information

        if isinstance(assignments, Assignment):
            assignments = [assignments]  # force list

        # collect all incomplete results make urls and feedback
        result_list = []
        feedback_list = []
        urls = []
        for cnt_ass, ass in enumerate(assignments):
            for cnt_res, res in enumerate(ass.results):
                if force_update or res.submissions_undefined:
                    result_list.append(res)
                    urls.append(ANSApi.make_url(what=f"results/{res.id}"))
                    feedback_list.append(
                        f"assignment {cnt_ass+1}/{len(assignments)}" +
                        f" - result {cnt_res+1}/{len(ass.results)}")
        for i, fb in enumerate(feedback_list):
            feedback_list[i] = f"[result submissions] {i+1}/{len(feedback_list)} " + fb

        if len(urls) == 0:
            return False

        chunck_size = 100
        i = 0
        while True:
            j = i + chunck_size
            responses = self._get_multiprocessing(
                urls[i:j], feedback_list=feedback_list[i:j])
            for res, rsp in zip(result_list[i:j], responses):
                res.update(rsp)
            i = j
            if i > len(result_list)-1:
                break
            self._save_intermediate()

        return True

    def downland_scores(self, assignments: Union[Assignment, List[Assignment]],
                        force_update=False) -> bool:
        if isinstance(assignments, Assignment):
            assignments = [assignments]  # force list

        result_list = []
        feedback_list = []
        urls = []
        for cnt_ass, ass in enumerate(assignments):
            for cnt_res, res in enumerate(ass.results):
                for cnt_sub, sub in enumerate(res.submissions):
                    if force_update or not sub.has_scores():
                        result_list.append(sub)
                        urls.append(ANSApi.make_url(
                            what=f"submissions/{sub.id}"))
                        feedback_list.append(
                            f"ass {cnt_ass+1}/{len(assignments)}" +
                            f" - res {cnt_res+1}/{len(ass.results)}" +
                            f" - submission {cnt_sub+1}")
        for i, fb in enumerate(feedback_list):
            feedback_list[i] = f"[result answer details] {i+1}/{len(feedback_list)} " + fb

        if len(urls) == 0:
            return False

        chunck_size = 100
        i = 0
        while True:
            j = i + chunck_size
            responses = self._get_multiprocessing(
                urls[i:j], feedback_list=feedback_list[i:j])

            for sub, rsp in zip(result_list[i:j], responses):
                sub.update(rsp)
            i = j
            if i > len(result_list)-1:
                break
            self._save_intermediate()

        return True


    def _get_multiprocessing(self, url_list: List[str],
                             ignore_http_error=False,
                             feedback_list: Optional[List[Optional[str]]] = None):
        # helper function to download from ANS
        # returns response that belong to the url_list

        self._check_token()
        rtn = []
        if feedback_list is None:
            feedback = itertools.cycle([None])
        else:
            feedback = feedback_list

        if self._n_threads < 2:
            # single thread
            for url, fb in zip(url_list, feedback):
                rsp = self.cache.get(url)
                if rsp is None:
                    # try retrieve online
                    rsp = self.get(url, ignore_http_error=ignore_http_error)
                if rsp is not None and len(rsp):
                    rtn.append(rsp)
                    if fb is not None:
                        self._feedback(fb)
        else:
            # multi thread
            proc_manager = rt.RequestProcessManager(self.cache,
                                                    max_processes=self._n_threads)
            rtn_dict = {}  # use dict, because response come in unpredicted order
            i = -1
            for url, fb in zip(url_list, feedback):
                i = i+1
                if i % INTERMEDIATE_SAVE == INTERMEDIATE_SAVE-1:
                    self._save_intermediate()
                rsp = self.cache.get(url)
                if fb is not None:
                    self._feedback(fb)
                if rsp is None:
                    # try retrieve online (add the thread list)
                    proc_manager.add(who=i,
                                     thread=rt.RequestProcess(url, headers=self.__auth_header,
                                                              ignore_http_error=ignore_http_error))
                else:
                    # from cache
                    rtn_dict[i] = rsp

                # read responses from threads
                while True:
                    for who, rsp in proc_manager.get_finished():
                        if rsp is not None:
                            rtn_dict[who] = rsp

                    if i < len(url_list)-1:
                        # always break, but for the last one (else)
                        # ensure that all threads are read before breaking
                        break
                    elif proc_manager.n_threads() == 0:
                        break

            # return list with correctly ordered responses
            rtn = []
            for i in range(len(url_list)):
                rtn.append(rtn_dict[i])

        return rtn

    def _get_multiprocessing_multipages(self, what_list: List[str],
                                        items: int = 100,
                                        feedback_list: Optional[List[Optional[str]]] = None):
        # helper function to download from ANS
        # returns response that belong to the url_list

        self._check_token()
        rtn = []
        if feedback_list is None:
            feedback = itertools.cycle([None])
        else:
            feedback = feedback_list

        if self._n_threads < 2:
            # single thread
            for what, fb in zip(what_list, feedback):
                rsp = self.get_multiple_pages(what=what, items=items)
                if rsp is not None and len(rsp):
                    rtn.append(rsp)
                    if fb is not None:
                        self._feedback(fb)
        else:
            # multi thread
            proc_manager = rt.RequestProcessManager(self.cache,
                                                    max_processes=self._n_threads)
            rtn_dict = {}  # use dict, because response come in unpredicted order
            i = -1
            for what, fb in zip(what_list, feedback):
                i = i + 1
                if i % INTERMEDIATE_SAVE == INTERMEDIATE_SAVE-1:
                    self._save_intermediate()
                url = self.make_url(what=what) + \
                    f"?items={items}" + "&page={{cnt:1}}"
                rsp = self.cache.get(url)
                if fb is not None:
                    self._feedback(fb)
                if rsp is None:
                    # try retrieve online (add the thread list)
                    proc_manager.add(who=i,
                                     thread=rt.MultiplePagesRequestProcess(url, headers=self.__auth_header))
                else:
                    # from cache
                    rtn_dict[i] = rsp

                # read responses from threads
                while True:
                    for who, rsp in proc_manager.get_finished():
                        if rsp is not None:
                            rtn_dict[who] = rsp

                    if i < len(what_list)-1:
                        # always break, but for the last one (else)
                        # ensure that all threads are read before breaking
                        break
                    elif proc_manager.n_threads() == 0:
                        break

            # return list with correctly ordered responses
            rtn = []
            for i in range(len(what_list)):
                rtn.append(rtn_dict[i])

        return rtn

    def _feedback(self, txt: str) -> None:
        print_feedback(txt, self.feedback_queue)
