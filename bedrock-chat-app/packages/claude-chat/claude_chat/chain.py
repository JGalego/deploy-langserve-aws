import os

# For a description of each inference parameter, please refer to
# https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-claude.html
_model_kwargs = {
    "temperature": float(os.getenv("BEDROCK_CLAUDE_TEMPERATURE", "0.1")),
    "top_p": float(os.getenv("BEDROCK_CLAUDE_TOP_P", "1")),
    "top_k": int(os.getenv("BEDROCK_CLAUDE_TOP_K", "250")),
    "max_tokens": int(os.getenv("BEDROCK_CLAUDE_MAX_TOKENS_TO_SAMPLE", "300")),
}

from langchain_aws import ChatBedrock
from langchain_core.runnables import ConfigurableField

# Full list of base model IDs is available at
# https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids-arns.html
_model_alts = {
    # As of June 2024, Claude 3.5 Sonnet is only available in N. Virginia (us-east-1)
    "claude_3.5_sonnet": ChatBedrock(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0", model_kwargs=_model_kwargs
    ),
    # As of April 2024, Claude 3 Opus is only available in Oregon (us-west-2)
    "claude_3_opus": ChatBedrock(
        model_id="anthropic.claude-3-opus-20240307-v1:0", model_kwargs=_model_kwargs
    ),
    "claude_3_haiku": ChatBedrock(
        model_id="anthropic.claude-3-haiku-20240307-v1:0", model_kwargs=_model_kwargs
    ),
    "claude_2_1": ChatBedrock(
        model_id="anthropic.claude-v2:1", model_kwargs=_model_kwargs
    ),
    "claude_2": ChatBedrock(
        model_id="anthropic.claude-v2", model_kwargs=_model_kwargs
    ),
    "claude_instant_1": ChatBedrock(
        model_id="anthropic.claude-instant-v1", model_kwargs=_model_kwargs
    ),
}

_model = ChatBedrock(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0", model_kwargs=_model_kwargs
).configurable_alternatives(
    which=ConfigurableField(
        id="model", name="Model", description="The model that will be used"
    ),
    default_key="claude_3_sonnet",
    **_model_alts,
)

from langchain_core.prompts import ChatPromptTemplate

# For some tips on how to construct effective prompts for Claude,
# check out Anthropic's Claude Prompt Engineering deck (Bedrock edition)
# https://docs.google.com/presentation/d/1tjvAebcEyR8la3EmVwvjC7PHR8gfSrcsGKfTPAaManw
_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are {role}."),
        ("human", "{input}"),
    ]
)

# For a quick intro to the LangChain Expression Language (LCEL), please refer to
# https://python.langchain.com/docs/expression_language/
chain = _prompt | _model
