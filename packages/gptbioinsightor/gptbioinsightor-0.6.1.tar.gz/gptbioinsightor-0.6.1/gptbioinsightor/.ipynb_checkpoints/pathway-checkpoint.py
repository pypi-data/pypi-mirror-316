
def design_term_text(terms, condition, source, lang="en"):
    def bg_text(condition, source):
        if condition is not None and source is not None:
            addition = f"Condition: Enriched from {condition} genes \nSource: {condition} genes are from {source}"
        elif condition is not None:
            addition = f"Condition: Enriched from {condition} genes"
        elif source is not None:
            addition = f"Source: genes are from {source}"
        else:
            addition = ""
        return addition
        
    language = lang if lang not in LANG_DIC else LANG_DIC[lang]}
    QUERY_PROMPT += f"Please return {language}"
    prompt = QUERY_PROMPT.format(addition=bg_text(condition, source), terms="\n".join(terms))
    return prompt


def inspire(
    terms, 
    condition=None, 
    source=None, 
    database=None, 
    provider='openai', 
    model='gpt-4o', 
    base_url=None,
    lang="en"):
    
    text = term_prompt(terms, condition, source, lang=lang)
    print(text)
    msg = [{"role": "user", "content": text}]
    response = query_model(msg, provider=provider, model=model, base_url=base_url)
    result = response.choices[0].message.content
    return result


def inspire_cmp(terms_ls, 
            condition=None, 
            history=None, 
            source=None, 
            database=None, 
            provider='openai', 
            model='gpt-4o', 
            base_url=None,
            lang="en"):
    for idxm terms in enumerate(terms_ls):
        
    result_up = inspire(terms_ls[0], base_url=base_url, context="up-regulatation")
    result_dw = inspire(terms_ls[1], base_url=base_url, context="down-regulatation")
    msg = [
        {"role": "user", "content": term_prompt(terms_ls[0], context,  lang="en")},
        {"role": "assistant", "content": result_up},
        {"role": "user", "content": term_prompt(terms_ls[1], context,  lang="en")},
        {"role": "assistant", "content": result_dw},
        {"role": "user", "content": "Hi, GPTBioInsightor! According to previous conversation, please analyse the difference impact for CTCs between up-regulatation and down-regulatation term. Please return Chinese "}
    ]
    response = query_model(msg, provider=provider, model=model, base_url=base_url) 
    result = response.choices[0].message.content.split('\n')
    return result
