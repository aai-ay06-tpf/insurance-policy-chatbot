from ml_service.web_scrapper import parent_document_retriever, qdrant_retriever



if __name__ == "__main__":


    searchs = [
        ("codigo_de_comercio", [524, 525, 526]),#, 538]),
        ("companias_de_seguros", [3, 10, 36]),
        ("protocolo_seguridad_sanitaria", [18]),
        ("codigo_sanitario", [112]),
        ("codigo_penal", [470])
    ]
    
    if True:
        try:
            # Doesn't work on Windows
            pd_retriever = parent_document_retriever(searchs)
        except Exception as e:
            print(e)
            
    
    # params 1
    # search_type = "similarity_score_threshold"
    # kwargs = dict(k=2, score_threshold=0.8)
    # retriever = qdrant_retriever(searchs, search_type, kwargs=kwargs)
    
    search_type="mmr"
    search_kwargs={'k': 3, 'lambda_mult': 0.25}
    retriever = qdrant_retriever(searchs, search_type, kwargs=search_kwargs)
    
    with open("retriever.txt", "a") as f:
        
        msg = input("query for retriever: ")
        response = retriever.invoke(msg)
        f.write(f"query: {msg}\n")
        f.write(f"response qdrant: {response}\n")
        response = pd_retriever.invoke(msg)        
        f.write(f"response pr_retriever: {response}\n")
        f.write("\n"+ "="*50+ "\n")
    
    