"""Verify submitted files and directories required by the spec."""

from pathlib import Path
import os
import bs4
import markdown


def test_files_exist():
    """Check for files and directories required by the spec."""
    assert Path("bin").exists()
    assert Path("bin/search").exists()
    assert Path("bin/index").exists()
    assert Path("bin/searchdb").exists()
    assert Path("bin/install").exists()
    assert Path("inverted_index/pipeline.sh").exists()
    assert Path("index_server").exists()
    assert Path("index_server/index").exists()
    assert Path("index_server/index/api").exists()
    assert Path("index_server/pyproject.toml").exists()
    assert Path(
        "index_server/index/inverted_index/inverted_index_0.txt"
    ).exists()
    assert Path(
        "index_server/index/inverted_index/inverted_index_1.txt"
    ).exists()
    assert Path(
        "index_server/index/inverted_index/inverted_index_2.txt"
    ).exists()
    assert Path("search_server").exists()
    assert Path("search_server/search/sql").exists()
    assert Path("search_server/search").exists()
    assert Path("search_server/search/views").exists()
    assert Path("search_server/pyproject.toml").exists()


def test_check_gai_survey():
    """Check for and validate GAI.md."""
    assert os.path.exists("GAI.md")

    with open("GAI.md", encoding="utf-8") as md_file:
        md_text = md_file.read()

    # Parse the HTML content
    html_text = markdown.markdown(md_text, extensions=["attr_list"])
    soup = bs4.BeautifulSoup(html_text, "html.parser")

    # Extract answers
    num_questions = 29
    answers = {}
    for i in range(1, num_questions+1):
        qid = f"Q{i:02d}"
        question = soup.find(id=qid)
        assert question, f"Failed to find {qid}"
        answer = question.find_next()
        text = answer.text.strip()
        if answer.name == "ul" and qid == "Q06":
            # Multiple selection
            answers.update(validate_muliple_selection(answer, qid))
        elif answer.name == "ul":
            # Multiple choice
            answers[qid] = validate_multiple_choice(answer, qid)
        elif answer.name == "p" and text.isdigit():
            # Numeric
            answers[qid] = int(text)
        else:
            # Text
            answers[qid] = text

    # Validate ULCS count
    for i in range(2, 5):  # Q2 - Q4 inclusive
        count = int(answers[f"Q0{i}"])
        assert 0 <= count <= 15

    # Assert valid free response answers
    free_reponse_qids = [
        "Q13",
        "Q15",
        "Q16",
        "Q20",
        "Q21",
        "Q25",
        "Q26"
    ]
    for qid in free_reponse_qids:
        assert answers[qid]
        assert answers[qid].upper() != "FIXME"


def validate_multiple_choice(ele, qid):
    """Validate multiple choice response and return answer."""
    assert ele.name == "ul"

    selection = ""
    for list_item in ele.find_all("li"):
        if list_item.text.lower().startswith("[x]"):
            assert not selection, f"Q{qid}: Expected one selection '[x]'"
            selection = list_item.text.replace("[x]", "").strip()
    assert selection

    return selection


def validate_muliple_selection(ele, qid):
    """Validate multiple selection response and return answer."""
    assert ele.name == "ul"

    selections = {}
    for i, list_item in enumerate(ele.find_all("li"), start=1):
        sub_qid = f"{qid}.{i}"
        if list_item.text.lower().startswith("[x]"):
            selections[sub_qid] = "Yes"
        else:
            selections[sub_qid] = "No"

    return selections
