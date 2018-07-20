# coding: mixt

from docutils.examples import internals
from typing import List

from mixt import Element, Required, html
from mixt.contrib.css import css_vars, render_css, Modes

from ... import datatypes
from ..generic import Details, htmlize_rst


def htmlize_summary(lines: List[str]):
    text = "\n".join(lines).strip()
    return htmlize_rst(text)


def htmlize_details(parts: List[List[str]]):
    text = "\n\n".join(["\n".join(para) for para in parts]).strip()
    return htmlize_rst(text)


class DocString(Element):
    class PropTypes:
        _class: str = "docstring"
        doc: Required[datatypes.SimpleDocString]
        hide_summary: bool = False
        hide_details: bool = False
        open: bool = False

    # noinspection PyUnresolvedReferences
    @css_vars(globals())
    @classmethod
    def render_pycss_global(cls, context):
        return {
            "details.docstring": {
                margin-top: 1*em,
                "> summary > p": {
                    margin-top: 0,
                    white-space: normal,
                    display: inline,
                },
                "> div.content > p:first-child": {
                    margin-top: 1*em,
                },
            },
        }

    @classmethod
    def render_css_global(cls, context):
        css = render_css((cls.render_pycss_global(context)))
        return f"""
/* <{cls.__module__}.{cls.__name__}> */
{css}
/* </{cls.__module__}.{cls.__name__}> */
"""

    def render(self, context):
        doc = self.doc

        summary = None
        details = None

        if not self.hide_summary:
            summary = htmlize_summary(doc.summary)

        if not self.hide_details:
            details = htmlize_details(doc.details)

        if summary and details:
            return <Details open={self.open}>
                <summary>{summary}</summary>
                {details}
            </Details>

        if summary:
            return <div>{summary}</div>

        if details:
            return <div>{details}</div>
