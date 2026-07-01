from app.prompts import (
    build_analysis_prompt,
    build_chat_prompt,
    build_considerations_prompt,
    build_key_points_prompt,
)


def _all_prompt_text() -> str:
    prompts = [
        build_analysis_prompt(
            analysis_task="Review the contract.",
            focus_agents=["Contract Analyst"],
        ),
        build_analysis_prompt(
            analysis_task=None,
            focus_agents=["Legal Researcher"],
            user_query="What does this clause mean?",
        ),
        build_key_points_prompt(
            previous_analysis="Prior analysis.",
            focus_agents=["Legal Strategist"],
        ),
        build_considerations_prompt(
            previous_analysis="Prior analysis.",
            focus_agents=["Legal Strategist"],
        ),
        build_chat_prompt(
            question="What should I ask next?",
            analysis_context="Analysis context.",
            key_points="Key points.",
            considerations="Considerations.",
        ),
    ]
    return "\n".join(prompts).lower()


def test_prompts_include_not_legal_advice_framing():
    assert "not legal advice" in _all_prompt_text()
    assert "research assistance" in _all_prompt_text()


def test_prompts_mark_user_content_as_untrusted():
    prompt_text = _all_prompt_text()

    assert "untrusted" in prompt_text
    assert "user-provided content" in prompt_text


def test_prompts_request_citations_or_source_references():
    prompt_text = _all_prompt_text()

    assert "citation" in prompt_text or "citations" in prompt_text
    assert "source references" in prompt_text


def test_prompts_do_not_contain_best_course_of_action():
    assert "best course of action" not in _all_prompt_text()
