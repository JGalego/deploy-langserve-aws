import os

# For a description of each inference parameter, please refer to
# https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-claude.html
_model_kwargs = {
    "temperature": float(os.getenv("BEDROCK_CLAUDE_TEMPERATURE", "0.1")),
    "top_p": float(os.getenv("BEDROCK_CLAUDE_TOP_P", "1")),
    "top_k": int(os.getenv("BEDROCK_CLAUDE_TOP_K", "250")),
    "max_tokens": int(os.getenv("BEDROCK_CLAUDE_MAX_TOKENS_TO_SAMPLE", "300")),
}

from langchain_community.chat_models import BedrockChat
from langchain.schema.runnable import ConfigurableField

# Full list of base model IDs is available at
# https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids-arns.html
_model_alts = {
    "claude_3_haiku": BedrockChat(
        model_id="anthropic.claude-3-haiku-20240307-v1:0", model_kwargs=_model_kwargs
    ),
    "claude_2_1": BedrockChat(
        model_id="anthropic.claude-v2:1", model_kwargs=_model_kwargs
    ),
    "claude_2": BedrockChat(
        model_id="anthropic.claude-v2", model_kwargs=_model_kwargs
    ),
    "claude_1": BedrockChat(
        model_id="anthropic.claude-v1", model_kwargs=_model_kwargs
    ),
    "claude_instant_1": BedrockChat(
        model_id="anthropic.claude-instant-v1", model_kwargs=_model_kwargs
    ),
}


_model = BedrockChat(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0", model_kwargs=_model_kwargs
).configurable_alternatives(
    which=ConfigurableField(
        id="model", name="Model", description="The model that will be used"
    ),
    default_key="claude_3_sonnet",
    **_model_alts,
)

from langchain.prompts import ChatPromptTemplate

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
