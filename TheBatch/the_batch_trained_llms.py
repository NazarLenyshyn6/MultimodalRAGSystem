from TheBatch.the_batch_llms import TheBatchLLM
from TheBatch.the_batch_configs import the_batch_prompt_template
from TheBatch.the_batch_vectorestore_pipeline import the_batch_vectorestore

the_batch_llm = TheBatchLLM(prompt_template=the_batch_prompt_template,
                            vectorstore=the_batch_vectorestore
                            )