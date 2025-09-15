from prompts import query_prompt_template

def write_query(question: str, db, llm):
    # Fill in the template
    prompt = query_prompt_template.invoke({
        "dialect": db.dialect,
        "top_k": 10,
        "table_info": db.get_table_info(),
        "input": question,
    })

    result = llm.invoke(prompt)

    return result.content