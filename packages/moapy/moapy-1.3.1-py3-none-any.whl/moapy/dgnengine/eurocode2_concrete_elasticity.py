from pydantic import Field, ConfigDict
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.designers_guide.resource.report_form import ReportForm
from moapy.designers_guide.func_general import DG_Result_Reports
from moapy.data_post import print_result_data

class Strength(MBaseModel):
    f_ck: float = Field(default=45.0, title="Characteristic cylinder strength",
                        json_schema_extra={"x-component-detail": {
                                            "symbol": {
                                                "type": "string",
                                                "default": r"f_{ck}"},
                                            "unit": {
                                                "type": "string",
                                                "default": "MPa"
                                            }}})
    model_config = ConfigDict(title="")

@auto_schema(title="Eurocode 2 Modulus of Elasticity",
             description= "Calculate modulus of elasticity from characteristic cylinder strength")
def report_ec2_concrete_elasticity(strength: Strength) -> DG_Result_Reports:
    E_cm: float = 22.0*pow(strength.f_ck/10.0, 0.3)
    result = ReportForm(title="Caculated modulus of elasticity",
                        formula=r"22[(f_{ck}+8)/10]^{0.3}",
                        symbol=r"E_{cm}",
                        result = E_cm,
                        unit = "GPa")
    results = { "result": [[ result.to_dict()]] }
    return DG_Result_Reports(res_report=results)

if __name__ == "__main__":
    str = Strength
    str.f_ck = 45.0
    print_result_data(report_ec2_concrete_elasticity(strength=str))