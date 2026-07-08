import argparse
import sys
from pathlib import Path

from app.analysis import ANALYSIS_CONFIGS, AnalysisRequest, run_analysis_request


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "analyze":
        return _analyze(args)

    parser.print_help()
    return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m app.cli",
        description="Run local legal document analysis demos.",
    )
    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a local text or Markdown document.",
    )
    analyze_parser.add_argument(
        "document_path",
        type=Path,
        help="Path to a local .txt or .md document.",
    )
    analyze_parser.add_argument(
        "--analysis-type",
        default="Contract Review",
        choices=sorted(ANALYSIS_CONFIGS),
        help="Analysis workflow to run.",
    )
    analyze_parser.add_argument(
        "--custom-query",
        help="Custom question to pass to the analysis workflow.",
    )
    analyze_parser.add_argument(
        "--mock",
        action="store_true",
        help="Run deterministic mock analysis without external services.",
    )
    return parser


def _analyze(args: argparse.Namespace) -> int:
    try:
        document_text = args.document_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Error: could not read {args.document_path}: {exc}", file=sys.stderr)
        return 1

    request = AnalysisRequest(
        document_text=document_text,
        analysis_type=args.analysis_type,
        custom_query=args.custom_query,
        app_mode="mock" if args.mock else "live",
    )

    try:
        result = run_analysis_request(request)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(
        _format_cli_summary(
            document_path=args.document_path,
            analysis_type=args.analysis_type,
            custom_query=args.custom_query,
            result=result,
        )
    )
    return 0


def _format_cli_summary(
    document_path: Path,
    analysis_type: str,
    custom_query: str | None,
    result: object,
) -> str:
    sections = [
        "Legal Agent Analysis",
        f"Document: {document_path}",
        f"Analysis type: {analysis_type}",
    ]
    if custom_query:
        sections.append(f"Custom query: {custom_query}")
    sections.extend(
        [
            "",
            "Summary",
            _response_content(result.response),
            "",
            "Key Points",
            _response_content(result.key_points_response),
            "",
            "Questions for a Qualified Legal Professional",
            _response_content(result.considerations_response),
        ]
    )
    return "\n".join(sections)


def _response_content(response: object) -> str:
    return getattr(response, "content", str(response)).strip()


if __name__ == "__main__":
    raise SystemExit(main())
