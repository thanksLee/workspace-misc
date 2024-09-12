import streamlit as st

from .model_analyze import ModelAnalyzeView
from .model_compare import ModelCompareView
from .model_specification import ModelSpecificationView
from .model_audit_analyze import ModelAuditAnalyzeView


class ModelQCMainView:
    def __init__(self):
        pass

    def model_analyze_view(self):
        ModelAnalyzeView().render()

    def model_compare_view(self):
        ModelCompareView().render()

    def model_specification_view(self):
        ModelSpecificationView().render()

    def model_audit_analyze_view(self):
        ModelAuditAnalyzeView().render()

    def render(self):
        st.write('VitaminStudio - Model QC Main')
