## Easy-LLMS
* Easy "1-line" calling of every LLM from OpenAI, MS Azure, AWS Bedrock, GCP Vertex, and Ollama

## Table of Contents
- [1.) What is Easy-LLMS and why would you use it](#1-what-is-easy-llms-and-why-would-you-use-it)
- [2.) Quick Getting Started](#2-quick-getting-started)
- [3.) Authentication](#3-authentication)
  - [OpenAI](#openai)
  - [Azure](#azure)
  - [AWS](#aws)
  - [Google](#google)
  - [Ollama](#ollama)
  - [Per Model Authentication](#per-model-authentication)
- [4.) Detailed Usage and Examples](#4-detailed-usage-and-examples)
  - [Easy "Import All" and call any Model](#easy-import-all-and-call-any-model)
  - [Passing Advanced Options](#passing-advanced-options)
  - [Loading Providers and Models more efficiently](#loading-providers-and-models-more-efficiently)
- [5.) Supported Providers and Models](#5-supported-providers-and-models)
- [6.) Assumptions](#6-assumptions)
- [7.) Help/Questions/Comments](#7-help-questions-comments)


## 1.) What is Easy-LLMS and why would you use it?
Easy-LLMS is a Python module which gives you easy "1-line" access to *every* LLM (Large Language Model) within OpenAI, MS Azure, AWS Bedrock, GCP Vertex, and Ollama

The idea is that you do not need to focus on the individual provider's APIs or LangChain abstractions, the different authentication methods, or the multitude of LLM requirements/options/parameters/documentation, etc. Rather, you can quickly interact and compare LLMs, get results, and build useful things with those LLMs.

If you find this helpful, I would very much appreciate starring it on GitHub.



## 2.) Quick Getting Started

### Install/Upgrade
* Install/upgrade latest via: `pip install -U easy-llms`

* Alternatively, install latest via: `pip install git+https://github.com/ventz/easy-llms`
* You can upgrade to the latest via: `pip install --upgrade --force-reinstall git+https://github.com/ventz/easy-llms`


### Example: OpenAI
Let's start with OpenAI since most are familiar with it:

```
from llms.openai import *

answer = gpt_4o().run("what llm are you?")
```

The authentication, in this case for OpenAI, is done in one of two
ways:

1.) Either by having the `OPENAI_API_KEY` ENV variable available in your environment

or

2.) Via having a `.llms` folder in the working directory, with a `openai` file inside of it, which contains `OPENAI_API_KEY="sk-..."`.


### Example: AWS Bedrock - Claude v3 Haiku
Next, let's switch to Claude v3 Haiku via AWS Bedrock.:


```
from llms.aws import *

answer = claude_3_haiku().run("what llm are you?")
```

The authentication, in this case for AWS Bedrock, is done in one of two
ways:

1.) Either by having the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY, and `AWS_REGION` ENV variables available in your environment

or

2.) Via having a `.llms` folder in the working directory, with an `aws` file inside of it, which contains `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY, and `AWS_REGION`.


### Example: Ollama - Llama3
Next, let's switch to Llama3 via Ollama:

Ollama does not export any LLMs. This is because it is technically a pass-through to any models that you have setup. 

This means you will *NOT* see it list any LLMs explicitly:
```
from llms import *
ollama.list()
```

What you would do in this case is pass the model directly to the
module, for example:

```
from llms import *

answer = ollama("llama3").run("what llm are you?")

By default, Ollama will use the "Chat" interface. If you have a model
that does not support Chat, you can disable chat:

answer = ollama("llama3", chat=False).run("what llm are you?")
```

While Ollama has no authentication, we use the "BASE_URL" instead and it is still done in one of two
ways:

1.) Either by having the `OLLAMA_BASE_URL` ENV variable available in your environment

or

2.) Via having a `.llms` folder in the working directory, with a `ollama` file inside of it, which contains `OLLAMA_BASE_URL="http://fqdn:11434"`


See [Authentication](#3-authentication) for more authentication information and examples.

See [Detailed Usage and Examples](#4-detailed-usage-and-examples) for more usage and options (including advanced parameters) options.



## 3.) Authentication

There are two ways of authenticating the various providers within Easy-LLMS:

1.) Via ENV variables

or

2.) Via `.llms` folder in the working directory, with a `openai` file, `azure` file, `aws` file, and `google` file, inside the llms directory, as needed.



Here are the AUTH requirements for each of the providers in ENV
variables and files (choose one, not both)

### OpenAI

1.) ENV variables:

`export OPENAI_API_KEY="sk-..."`

or

2.) `openai` file with:
```
OPENAI_API_KEY="sk-..."
```

NOTE: There is one more variable available: `OPENAI_BASE_URL`, and it
can be used to point at an OpenAI compatible proxy. (ex: LiteLLM)

It can be supplied as an ENV variable, or within the `openai` file.


### Azure

1.) ENV variables:

`export AZURE_OPENAI_API_KEY=...`

`export AZURE_OPENAI_API_VERSION="YYYY-MM-DD"`

`export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com"`

or

2.) `azure` file with:
```
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_API_VERSION="YYYY-MM-DD"
AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com"
```

### AWS

1.) ENV variables:

`export AWS_ACCESS_KEY_ID="AKIA..."`

`export AWS_SECRET_ACCESS_KEY="..."`

`export AWS_REGION="us-east-1"`

or

2.) `aws` file with:
```
AWS_ACCESS_KEY_ID="AKIA..."
AWS_SECRET_ACCESS_KEY="..."
AWS_REGION="us-east-1"
```

### Google

1.) ENV variables:

`export GCP_PROJECT_ID="project-name"`

`export GCP_REGION="us-central1"`

`export GCP_CREDENTIALS_JSON='{
"type": "service_account",
  "project_id": "project-name",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...=\n-----END PRIVATE KEY-----\n",
  "client_email": "project@project-name.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/project%40project-name.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}'`


or

2.) `google` file with:
```
GCP_PROJECT_ID="project-name"
GCP_REGION="us-central1"
GCP_CREDENTIALS_JSON='{
"type": "service_account",
  "project_id": "project-name",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...=\n-----END PRIVATE KEY-----\n",
  "client_email": "project@project-name.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/project%40project-name.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}'
```


### Ollama

1.) ENV variables:

`export OLLAMA_BASE_URL="http://fqdn:11434"`

or

2.) `ollama` file with:
```
OLLAMA_BASE_URL="http://fqdn:11434"
```

## Per Model Authentication

You can override the auth for a specific model by using the `.llms/provider-model` structure, where `provider` is one of: `openai`, `azure`, `google`, and `ollama`, and model is any of the
models via `provider.list()`

For example, to override the auth for "Claude 3 Opus", since the model
name is `claude_3_opus` and it's from `aws`, you can create a `.llm/aws-claude_3_opus` config.

Or, to override the auth for "Titan Premier", since the model name is `titan_premier_v1` and it's from `aws`, you can create a `.llm/aws-titan_premier_v1` config.

Other than being able to authenticate a specific LLM with different credentials, this is especially useful for certain models that are only available in specific regions (ex: Claude 3 Opus in "us-west-2", and Titan Premier in "us-east-1")

For Ollama, again it is worth noting that since it does not export any LLMs, in order to auth a specific model to a specific Ollama instance, you need to pass the `model_auth=True` parameter manually, for example:

```
from llms import *

question = "Who was the first person to step on the moon?"

answer = ollama("llama3", model_auth=True).run(question)
```

This will look for a `.llms/ollama-llama3` config.

## 4.) Detailed Usage and Examples

1.) Look at [Supported Providers and Models](#5-supported-providers-and-models) to get a list of Providers and Models - a one time task!

2.) Then make sure you have setup the proper [Authentication](#3-authentication) - a one time task!

3.) The easiest and quickest way to use everything:

### Easy "Import All" and call any Model
```
from llms import *

```

From here, you can call any provider/model available to you:

```
answer = gpt_4o().run("what llm are you?")
```

or

```
answer = claude_3_haiku().run("what llm are you?")
```

For example, you can run one question against multiple providers like
this:

```
from llms import *

question = "Who was the first person to step on the moon?"

# OpenAI
answer = gpt_4o().run(question)

# AWS
answer = claude_3_haiku().run(question)

# Google
answer = gemini_pro_1_5().run(question)
```

It is worth noting again for that Ollama, you will specify the model
directly, such as:

```
from llms import *

question = "Who was the first person to step on the moon?"

answer = ollama("llama3").run(question)

answer = ollama("mistral").run(question)
```

And again, if your Ollama model does not support "Chat", you can specify it without Chat:

```
from llms import *

question = "Who was the first person to step on the moon?"

answer = ollama("command-r-plus", chat=False).run(question)
```





### Passing Advanced Options

You can pass *every* option/parameter that each provider and model supports.

Two widely used options/parameters are "wrapped" for you as:

* `temperature`
and
* `max_tokens`

For example:
```
answer = gpt_4o(temperature=1, max_tokens=100).run("what llm are you?")
```

You can pass any other option available, for example:

```
answer = gpt_4o(top_p=1).run("what llm are you?")
```

And:

```
answer = gpt_4o(top_p=1, presence_penalty=1, frequency_penalty=1).run("what llm are you?")
```

For Ollama, it's as simple as:

```
answer = ollama("llama3", top_p=1, presence_penalty=1, frequency_penalty=1).run("what llm are you?")
```




### Loading Providers and Models more efficiently

If you are only working with one provider, you can only load that
provider. For example, you only need OpenAI, you can:

```
from llms.openai import *
answer = gpt_4o().run(...)
```

You can do the same with Azure:

```
from llms.azure import *
```

or AWS:

```
from llms.aws import *
```

or Google:

```
from llms.google import *
```


You can further narrow it down to one model. For example, let's say
you only need "gpt-4o" from OpenAI, you can load it as:
```
from llms.openai import gpt_4o
answer = gpt_4o().run(...)
```


Again, Ollama is the only one that you *CANNOT* load with:
```
from llms.ollama import *
answer = ollama("llama3").run(...)
```

This is due to Ollama not exporting any LLMs.

You would have load it with:
```
from llms import ollama
answer = ollama("llama3").run(...)
```



## 5.) Supported Providers and Models

You can list out the models with:

```
from llms import llms
print(llms.list())
```

Which will produce:
```
['openai', 'azure', 'aws', 'google', 'ollama']
```

And from there, you can list each as:

```
from llms import openai
print(openai.list())

from llms import azure
print(azure.list())

from llms import aws
print(aws.list())

from llms import google
print(google.list())

# NOTE: Ollama does not export any LLMs.
#       This is because it is technically a pass-through to any models that you have setup. 
#       That means you will see an empty list "[]" of exported LLMs 
from llms import ollama
print(ollama.list())

```

Which will produce the models you can use:
```
['gpt_35_turbo', 'gpt_35_turbo_16k', 'gpt_4_turbo', 'gpt_4o', 'gpt_4o_mini', 'gpt_4', 'gpt_4_32k']

['azure_gpt_35_turbo', 'azure_gpt_35_turbo_16k', 'azure_gpt_4_turbo', 'azure_gpt_4', 'azure_gpt_4_32k']

['claude_3_haiku', 'claude_3_sonnet', 'claude_3_opus', 'claude_35_sonnet', 'claude_1_instant', 'claude_1', 'llama2_70b', 'llama3_8b_instruct', 'llama3_70b_instruct', 'llama3_1_8b_instruct', 'llama3_1_70b_instruct', 'llama3_1_405b_instruct', 'mistral_7b_instruct', 'mistral_large', 'mistral_large_2', 'mistral_small', 'mixtral_8x7b_instruct', 'cohere_command_14', 'cohere_command_light_14', 'j2_mid', 'j2_ultra', 'titan_lite_v1', 'titan_express_v1', 'titan_premier_v1']

['gemini_pro_1', 'gemini_pro_1_5', 'gemini_flash_1_5', 'bison', 'bison_32k']

# NOTE: Ollama is empty due to not exporting any LLMs
[]
```



Here is a user-friendly list of the models across OpenAI, Azure, AWS, Google, and Ollama, however do note that these are NOT the model names that you would use within Easy-LLMS:

```
# AWS Anthropic:
* claude-3-haiku
* claude-3-sonnet
* claude_35_sonnet
* claude-3-opus [note: currently only available in 'us-east-2']
* claude-v2
* claude-instant

# AWS Meta:
* llama2-13b
* llama2-70b
* llama3-8b
* llama3-70b
* llama3.1-8b
* llama3.1-70b
* llama3.1-405b

# AWS Mistral and Mixtral:
* mistral-7b-instruct
* mistral-large
* mistral-large-2
* mistral-small
* mixtral-8x7b-instruct
* mixtral-large

# AWS Cohere:
* cohere-command-v14
* cohere-command-light-v14
* [support coming soon] cohere.command-r-v1:0
* [support coming soon] cohere.command-r-plus-v1:0

# AWS AI21 Labs:
* ai21-j2-mid
* ai21-j2-ultra

# AWS Amazon (Titan):
* amazon-titan-lite
* amazon-titan-express
* amazon-titan-premier [note: currently only available in 'us-east-1']

# MS Azure:
* azure-gpt-4-turbo-preview
* azure-gpt-3.5-turbo
* azure-gpt-4o
* azure-gpt-4
* azure-gpt-3.5-turbo-16k
* azure-gpt-4-32k

# OpenAI:
* gpt-4-turbo
* gpt-4-turbo-preview
* gpt-3.5-turbo
* gpt-4o
* gpt-4o-mini
* gpt-4
* gpt-3.5-turbo-16k
* gpt-4-32k

# Google Vertex:
* google-chat-bison
* google-chat-bison-32k
* google-gemini-pro-1.0
* google-gemini-pro-1.5-preview [note: currently only available in 'us-central1']
* google-gemini-flash-1.5-preview [note: currently only available in 'us-central1']

# Ollama
# https://ollama.com/library
* Any "Chat" model
* Any "Invoke" model
```


## 6.) Assumptions?

* You have python3 (ideally 3.11.x+, although it should work 3.6.x+)

* You have a python venv setup

* You have `pip install wheel` in your venv

* You have installed Easy-LLMS: `pip install easy-llms` or `pip install git+https://github.com/ventz/easy-llms`

* You have API access to the providers/models you want to use: OpenAI; MS Azure; AWS Bedrock; Google Vertex; Ollama
See [Supported Providers and Models](#supported-providers-and-models) for more information.


## 7.) Help/Questions/Comments
Please feel free to open GitHub Issues for all Questions and Comments.
PRs are always welcome and encouraged! The goal is to make this project better!
