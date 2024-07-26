# aws/__init__.py
from .claude3haiku import Claude3Haiku as claude_3_haiku
from .claude3sonnet import Claude3Sonnet as claude_3_sonnet
from .claude3opus import Claude3Opus as claude_3_opus
from .claude35sonnet import Claude35Sonnet as claude_35_sonnet
from .claude1instant import Claude1Instant as claude_1_instant
from .claude2 import Claude2 as claude_2
from .llama270b import Llama270b as llama2_70b
from .llama38binstruct import Llama38bInstruct as llama3_8b_instruct
from .llama370binstruct import Llama370bInstruct as llama3_70b_instruct
from .llama318binstruct import Llama318bInstruct as llama3_1_8b_instruct
from .llama3170binstruct import Llama3170bInstruct as llama3_1_70b_instruct
from .llama31405binstruct import Llama31405bInstruct as llama3_1_405b_instruct
from .mistral7binstruct import Mistral7bInstruct as mistral_7b_instruct
from .mistrallarge import MistralLarge as mistral_large
from .mistrallarge2 import MistralLarge2 as mistral_large_2
from .mistralsmall import MistralSmall as mistral_small
from .mixtral8x7binstruct import Mixtral8x7bInstruct as mixtral_8x7b_instruct
from .coherecommand14 import CohereCommand14 as cohere_command_14
from .coherecommandlight14 import CohereCommandLight14 as cohere_command_light_14
#from .coherecommandr import CohereCommandR as coherecommand_r
#from .coherecommandrplus import CohereCommandRPlus as coherecommand_r_plus
from .j2mid import J2Mid as j2_mid
from .j2ultra import J2Ultra as j2_ultra
#from .j2jambainstruct import J2JambaInstruct as j2_jamba_instruct
from .titanlitev1 import TitanLiteV1 as titan_lite_v1
from .titanexpressv1 import TitanExpressV1 as titan_express_v1
from .titanpremierv1 import TitanPremierV1 as titan_premier_v1
from .aws import AWS

__all__ = ['claude_3_haiku', 'claude_3_sonnet', 'claude_3_opus', 'claude_35_sonnet', 'claude_1_instant', 'claude_2', 'llama2_70b', 'llama3_8b_instruct', 'llama3_70b_instruct', 'llama3_1_8b_instruct', 'llama3_1_70b_instruct', 'llama3_1_405b_instruct', 'mistral_7b_instruct', 'mistral_large', 'mistral_large_2', 'mistral_small', 'mixtral_8x7b_instruct', 'cohere_command_14', 'cohere_command_light_14', 'j2_mid', 'j2_ultra', 'titan_lite_v1', 'titan_express_v1', 'titan_premier_v1']
