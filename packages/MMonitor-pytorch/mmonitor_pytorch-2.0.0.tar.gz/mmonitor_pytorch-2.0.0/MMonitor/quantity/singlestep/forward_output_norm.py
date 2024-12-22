from .base_class import SingleStepQuantity
from ...extensions import ForwardOutputExtension


class ForwardOutputNorm(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.output
        return data.norm(2)

    def forward_extensions(self):
        extensions = [ForwardOutputExtension()]
        return extensions

