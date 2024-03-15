from ml_service.web_scrapper import parent_document_retriever, qdrant_retriever



if __name__ == "__main__":


    searchs = [
        ("codigo_de_comercio", [524, 525, 526]),
        ("companias_de_seguros", [3, 10, 36]),
        ("protocolo_seguridad_sanitaria", [18]),
        ("codigo_sanitario", [112]),
        ("codigo_penal", [470])
    ]
    
    if False:
        # Doesn't work
        try:
            pr_retriever = parent_document_retriever(searchs)
        except Exception as e:
            print(e)
            
    
    search_type = "similarity_score_threshold"
    kwargs = dict(k=2, score_threshold=0.8)
    
    retriever = qdrant_retriever(searchs, search_type, kwargs=kwargs)
    
    
    with open("retriever.txt", "a") as f:
        
        msg = input("query for retriever: ")
        response = retriever.invoke(msg)
        # response = vectorstore.similarity_search_with_score(msg)
        
        f.write(f"query: {msg}\n")
        f.write(f"response: {response}\n")
        f.write("\n"+ "="*50+ "\n")
    
    