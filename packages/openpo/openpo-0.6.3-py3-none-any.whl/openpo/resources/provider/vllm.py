from typing import List, Union


class VLLM:
    def __init__(
        self,
        model: str,
        **vllm_kwargs,
    ) -> None:
        try:
            from vllm import LLM, SamplingParams
        except ImportError:
            raise ImportError(
                "vLLM requires additional dependencies. Install with: pip install openpo[eval]"
            )

        self.model = LLM(
            model=model,
            **vllm_kwargs,
        )

    def validate_vllm(self):
        return True

    def completions(
        self,
        prompts: List[str],
        use_tqdm: bool = True,
        **kwargs: Union[int, float, str],
    ) -> List[str]:
        prompts = [prompt.strip() for prompt in prompts]
        params = SamplingParams(**kwargs)

        outputs = self.model.generate(prompts, params, use_tqdm=use_tqdm)
        outputs = [output.outputs[0].text for output in outputs]
        return outputs
