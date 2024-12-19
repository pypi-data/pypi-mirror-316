import json
from typing import Any, Dict, Iterable, List, Optional, Tuple
from collections import OrderedDict

import pandas as pd

from .list_of_dicts import dataframe_from_list_of_dict
from .._misc import move_column_to_front
FIRST_OPTION_CORRECT = ord("A")
FIRST_OPTION_INCORRECT = ord("a")


class ANSObject(object):

    def __init__(self, dict_: Dict[str, Any]) -> None:
        self._dict = dict_
        self._sort_by = None
        self._order = None

    @property
    def dict(self) -> dict:
        return self._dict

    @property
    def id(self) -> str:
        return self._dict["id"]

    def json(self, indent: int = 2) -> str:
        return json.dumps(self._dict, indent=indent)

    def __str__(self) -> str:
        return self.json()

    def _set_ordering(self, order: Optional[List[str]], sort_key: Optional[str]) -> None:
        self._sort_by = sort_key
        if order is not None:
            self._order = {key: i for i, key in enumerate(order)}
        else:
            self._order = None

    def _reset_ordering(self) -> None:
        self._sort_by = None
        self._order = None

    def get_dict(self, key):
        return self._dict[key]


class InsightsQuestion(ANSObject):

    @property
    def p_value(self) -> Optional[float]:
        try:
            return self._dict["p_value"]
        except KeyError:
            return None

    @property
    def rit_value(self) -> Optional[float]:
        try:
            return self._dict["rit_value"]
        except KeyError:
            return None

    @property
    def rir_value(self) -> Optional[float]:
        try:
            return self._dict["rir_value"]
        except KeyError:
            return None


class InsightsAssignment(ANSObject):

    @property
    def participants(self) -> Optional[int]:
        try:
            return self._dict["participants"]
        except KeyError:
            return None

    @property
    def kr20(self) -> Optional[float]:
        try:
            return self._dict["kr20"]
        except KeyError:
            return None

    @property
    def pass_rate(self) -> Optional[float]:
        try:
            return self._dict["pass_rate"]
        except KeyError:
            return None


class Question(ANSObject):

    def __init__(self, dict_: Dict[str, Any]) -> None:
        super().__init__(dict_)
        self._insights = None
        self.insights_undefined = True

    @property
    def category(self) -> str:
        try:
            return self._dict["category"]
        except KeyError:
            return "?"

    @property
    def choice_type(self) -> str:
        try:
            return self._dict["choice_type"]
        except KeyError:
            return "?"

    @property
    def bonus(self) -> Optional[bool]:
        try:
            return self._dict["bonus"]
        except KeyError:
            return None

    @property
    def position(self):
        return int(self._dict["position"])

    @property
    def points(self) -> float:
        try:
            return float(self._dict["position"])
        except KeyError:
            return 0.0

    @property
    def insights(self) -> Optional[InsightsQuestion]:
        return self._insights

    @insights.setter
    def insights(self, val: Optional[InsightsQuestion]):
        self._insights = val
        self.insights_undefined = False


class Exercise(ANSObject):

    def __init__(self, dict_: Dict[str, Any]) -> None:
        super().__init__(dict_)
        self._questions = []

    @property
    def questions(self) -> List[Question]:
        return self._questions

    @questions.setter
    def questions(self, val: List[Question]):
        self._questions = val


class Course(ANSObject):

    @property
    def name(self) -> str:
        return self._dict["name"]

    @property
    def year(self) -> Optional[int]:
        return int(self._dict["year"])

    @property
    def course_code(self) -> str:
        return self._dict["course_code"]

    @property
    def instructor_names(self) -> Optional[list]:
        instr = []
        for i in self._dict["instructors"]:
            instr.append(i["first_name"] + " " + i["last_name"])
        return instr

    @property
    def all_instructors(self) -> str:
        rtn = ""
        for i in self._dict["instructors"]:
            rtn = rtn + i["last_name"] + ", "
        if len(rtn):
            rtn = rtn[:-2]
        return rtn

    @property
    def instructor_ids(self) -> Optional[list]:
        instr = []
        for i in self._dict["instructors"]:
            instr.append(i["external_id"])
        return instr


class Submission(ANSObject):

    @property
    def score(self) -> Optional[float]:
        try:
            return float(self._dict["score"])
        except (KeyError, ValueError, TypeError):
            return None

    def has_scores(self) -> bool:
        # all scores of the MC options
        return "scores" in self._dict

    @property
    def scores(self) -> Iterable[Dict[str, Any]]:  # different MC options
        if not self.has_scores():
            return []
        elif self._sort_by is None:
            return iter(self._dict["scores"])
        elif isinstance(self._order, list):
            return sorted(self._dict["scores"],
                          key=lambda x: self._order[x[self._sort_by]])  # type: ignore
        else:

            return sorted(self._dict["scores"],
                          key=lambda x: x[self._sort_by])   # type: ignore

    def get_choices(self) -> List[bool]:  # basically converted scores
        try:
            return [s["selected"] for s in self.scores]
        except KeyError:
            return []

    def get_answer_letter(self) -> str:
        try:
            c = self.get_choices().index(True)  # find correct
        except ValueError:
            return "."

        if self.score is not None and self.score > 0:  # correct answer
            return chr(c + FIRST_OPTION_CORRECT)
        else:
            return chr(c + FIRST_OPTION_INCORRECT)

    def set_scores_order(self, order=None) -> None:
        self._set_ordering(order=order, sort_key="choice_id")

    def reset_scores_order(self) -> None:
        self._reset_ordering()

    def update(self, dict_: dict) -> None:
        self._dict = dict_


class Result(ANSObject):

    def __init__(self, dict_: Dict[str, Any]) -> None:
        super().__init__(dict_)
        self._submissions = []
        self.submissions_undefined = True

    @property
    def grade(self):
        try:
            return float(self.dict["grade"])
        except (TypeError, KeyError):
            return None

    @property
    def total_points(self):
        try:
            return float(self.dict["total_points"])
        except (TypeError, KeyError):
            return None

    @property
    def submissions(self) -> Iterable[Submission]:
        # return an iter
        if len(self._submissions) == 0:
            return iter(self._submissions)
        elif self._sort_by is None:
            return iter(self._submissions)
        elif self._order is None:
            # type: ignore
            return sorted(self._submissions, key=lambda x: x._dict[self._sort_by])
        else:
            return sorted(self._submissions,
                          key=lambda x: self._order[x._dict[self._sort_by]])  # type: ignore

    @submissions.setter
    def submissions(self, val: List[Submission]):
        self._submissions = val
        self.submissions_undefined = False

    @property
    def users(self) -> List[Dict]:
        try:
            return self.dict["users"]
        except KeyError:
            return []

    def get_submissions_df(self,n_choices:int=0) -> pd.DataFrame:
        lst = []

        choice_cols = [f"choice_{i+1}" for i in range(n_choices)]
        for p, a in enumerate(self.submissions):
            d = a._dict
            d["position"] = p
            if n_choices > 0:
                ch = a.get_choices()
                for i, col in enumerate(choice_cols):
                    try:
                        resp = int(ch[i])
                    except IndexError:
                        resp = None
                    d[col] = resp

            d["scores"] = None # delete scores, that is, delete raw data of choices
            lst.append(d)

        rtn = dataframe_from_list_of_dict(lst, nested=False).convert_dtypes()
        select_cols = ["position", "exercise_id", "question_id", "score", "raw_score", "adjustment", "auto_graded"]
        select_cols.extend(choice_cols)

        return rtn.loc[:, select_cols]

    def get_exercise_scores(self) -> List[Optional[float]]:
        return [a.score for a in self.submissions]

    def get_choices(self) -> List[List[bool]]:
        return [a.get_choices() for a in self.submissions]

    def get_binary_score_string(self) -> str:
        rtn = []
        for a in self.submissions:
            if a.score is None:
                rtn.append("?")
            elif a.score > 0:
                rtn.append("1")
            else:
                rtn.append(".")
        return "".join(rtn)

    def get_answer_string(self) -> str:
        return "".join([a.get_answer_letter() for a in self.submissions])

    def set_submission_order(self, order: Optional[List[str]] = None) -> None:
        self._set_ordering(order=order, sort_key="exercise_id")

    def reset_submission_order(self):
        self._reset_ordering()

    def set_submission_scores_order(self, order: Optional[List[str]] = None) -> None:
        # set the order of all scores (answer options) of all
        # submission (questions)
        for s in self._submissions:
            s.set_scores_order(order=order)

    def reset_submission_scores_order(self) -> None:
        for s in self._submissions:
            s.reset_scores_order()

    def update(self, dict_: dict) -> None:
        self._dict = dict_
        if "submissions" in self._dict:
            self.submissions = [Submission(obj)
                                for obj in self._dict["submissions"]]


class Assignment(ANSObject):

    def __init__(self, dict_: Dict[str, Any]) -> None:
        super().__init__(dict_)
        self._results = []
        self._exercises = []
        self._course = None
        self._insight = None
        self.results_undefined = True

    def __str__(self) -> str:
        return "Assignment {}, course_id={}, name='{}'".format(self.id,
                                                               self._dict["course_id"], self._dict["name"])

    @property
    def course(self) -> Optional[Course]:
        return self._course

    @course.setter
    def course(self, val: Optional[Course]):
        self._course = val

    @property
    def insights(self) -> Optional[InsightsAssignment]:
        return self._insight

    @insights.setter
    def insights(self, val: Optional[InsightsAssignment]):
        self._insight = val

    @property
    def exercises(self) -> List[Exercise]:
        return self._exercises

    @exercises.setter
    def exercises(self, val: List[Exercise]):
        self._exercises = val

    @property
    def results(self) -> List[Result]:
        return self._results

    @results.setter
    def results(self, val: List[Result]):
        self._results = val
        self.results_undefined = False

    @property
    # list of all questions of all exercises
    def questions(self) -> List[Question]:
        # return [q for quests in self._exercises for q in quests]
        rtn = []  # flat list
        for ex in self._exercises:
            for q in ex.questions:
                rtn.append(q)
        return rtn

    @property
    def open_questions(self) -> List[Question]:
        return list(filter(lambda x: x.category == "open", self.questions))

    @property
    def mc_questions(self) -> List[Question]:
        return list(filter(lambda x: x.category == "choice", self.questions))

    @property
    def points_mc(self) -> float:
        return sum([q.points for q in self.mc_questions])

    @property
    def points_open(self) -> float:
        return sum([q.points for q in self.open_questions])

    @property
    def points_total(self) -> float:
        return sum([q.points for q in self.questions])

    @property
    def name(self):  # list of questions of all exercises
        return self._dict["name"]

    @property
    def language(self):
        name = self._dict["name"]
        eng = name.find(" EN") > 0 or name.find(
            "-EN") > 0 or name.upper().find("ENGLISH") > 0
        nl = name.find(" NL") > 0 or name.find(
            "-NL") > 0 or name.upper().find("DUTCH") > 0
        if eng == nl:
            return "??"  # unclear, evidence for both or none
        elif eng:
            return "EN"
        else:
            return "NL"

    @property
    def resit(self):
        n = self._dict["name"].lower()
        return n.find(" hertentamen") > 0 or n.find(" resit") > 0

    @property
    def online(self):
        n = self._dict["name"].lower()
        return n.find(" online") > 0 or n.find(" proctored") > 0

    @property
    def results_ids(self) -> List[str]:
        return [r.id for r in self.results]

    def grades_dataframe(self, raw_ans_data: bool = False) -> pd.DataFrame:
        if raw_ans_data:
            return dataframe_from_list_of_dict([a.dict for a in self.results], nested=True)
        else:
            # result df
            data = []
            for r in self.results:
                if len(r.users) > 0:
                    stud = r.users[0]["student_number"]
                else:
                    stud = None
                code, cname, _ = self.course_info()
                row = {"course_id": self._dict["course_id"],
                       "course_code": code,
                       "assignment_id": self.id,
                       "student": stud,
                       "grade": r.grade,
                       "total_points": r.total_points,
                       "questions": r.get_binary_score_string(),
                       "course_name": cname}
                data.append(row)

            rtn = pd.DataFrame(data).convert_dtypes()
            if len(rtn) > 0:
                rtn.grade = pd.to_numeric(rtn.grade)
                rtn.total_points = pd.to_numeric(rtn.total_points)

            return rtn

    def submissions_dataframe(self, n_choices:int=0) -> pd.DataFrame:
        tmp = []
        for r in self.results:
            df = r.get_submissions_df(n_choices)
            df["assignment_id"] = self.id
            if len(r.users) > 0:
                df["stud"] = r.users[0]["student_number"]
            else:
                df["stud"] = -1

            code, _, _ = self.course_info()
            df["course_code"] = code
            tmp.append(df)
        try:
            rtn = pd.concat(tmp, axis=0, ignore_index=True)
        except ValueError:
            return pd.DataFrame()
        rtn = move_column_to_front(rtn, "assignment_id")
        rtn = move_column_to_front(rtn, "stud")
        return rtn

    def course_info(self) -> Tuple[str, str, str]:
        if isinstance(self.course, Course):
            name = self.course.name
            code = self.course.course_code
            instr = self.course.all_instructors
            return code, name, instr
        else:
            return "", "", ""

    def dataframe(self, raw_ans_data: bool = False) -> pd.DataFrame:
        if not raw_ans_data:
            d = self._dict
            d["n_exercises"] = len(self.exercises)
            d["n_questions"] = len(self.questions)
            d["lang"] = self.language
            d["online"] = int(self.online)
            d["resit"] = int(self.resit)
            if isinstance(self.course, Course):
                d["course_name"] = self.course.name
                d["course_code"] = self.course.course_code
            else:
                d["course_name"] = ""
                d["course_code"] = ""
            d["n_open"] = len(self.open_questions)
            d["n_mc"] = len(self.mc_questions)
            d["points_open"] = self.points_open
            d["points_mc"] = self.points_mc
            d["points_total"] = self.points_total

            if isinstance(self.insights, InsightsAssignment):
                d["participants"] = self.insights.participants
                d["kr20"] = self.insights.kr20
                d["pass_rate"] = self.insights.pass_rate
            else:
                d["participants"] = 0
                d["kr20"] = 0
                d["pass_rate"] = 0

            return dataframe_from_list_of_dict(
                [d],
                columns=["id", "course_id", "n_exercises", "n_questions", "resit",
                         "lang", "online", "n_mc", "n_open", "points_total",
                         "points_mc", "points_open",
                         "participants", "kr20", "pass_rate",
                         "course_code", "name", "course_name"],
                nested=False).convert_dtypes()
        else:
            return dataframe_from_list_of_dict([self._dict],
                                               nested=True).convert_dtypes()

    # list of all questions of all exercises
    def questions_dataframe(self) -> pd.DataFrame:
        rtn = []
        for q in self.questions:
            d = OrderedDict()
            d["assignment"] = self.id
            d["category"] = q.category
            d["choice_type"] = q.choice_type
            d["points"] = q.points
            d["position"] = q.position
            d["bonus"] = q.bonus
            if isinstance(q.insights, InsightsAssignment):
                d["p_value"] = q.insights.p_value
                d["rir_value"] = q.insights.rir_value
                d["rit_value"] = q.insights.rit_value
            else:
                d["p_value"] = 0
                d["rir_value"] = 0
                d["rit_value"] = 0

            rtn.append(d)
        return dataframe_from_list_of_dict(rtn)

    def n_results(self) -> int:
        return len(self._results)

    def order_all_questions_and_choices(self, reference_submission: Optional[Submission] = None) -> Optional[Submission]:
        if len(self._results) == 0:
            return
        if isinstance(reference_submission, Submission):
            ref_sub = [reference_submission]
        else:
            ref_sub = self.results[0].submissions  # take first on

        order = [s._dict["exercise_id"] for s in ref_sub]
        for r in self.results:
            # set all submissions to the same question order
            r.set_submission_order(order)
            r.set_submission_scores_order()  # set all choices of all question in same order

    def formated_label(self):
        if isinstance(self.course, Course):
            txt = f"{self.course.course_code[:14]:<14} {self.course.name[:40]:<40}"
        else:
            txt = "<no course info>"
        return f"{txt} {self.name}"
