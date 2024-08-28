import streamlit as st

from sample_01.modelqc.views.model_analyze_page import ModelAnalyzePage
from sample_01.modelqc.views.model_compare_page import ModelComparePage
from sample_01.modelqc.views.model_specification_page import ModelSpecificationPage
from sample_01.modelqc.views.model_audit_analyze_page import ModelAuditAnalyzePage


class ModelQCMainPage:
    def __init__(self):
        pass

    def model_analyze_page(self):
        ModelAnalyzePage().render()

    def model_compare_page(self):
        ModelComparePage().render()

    def model_specification_page(self):
        ModelSpecificationPage().render()

    def model_audit_analyze_page(self):
        ModelAuditAnalyzePage().render()

    def render(self):
        st.write('VitaminStudio - ModelQC Main')
