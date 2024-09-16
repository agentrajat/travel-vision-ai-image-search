from indexing import Indexing
from retrieval_models import BaseModel, BM25Model
from typing import List
# import io
# import base64

class IRSystem:
    def __init__(self, search_data: str, image_dir: str, object_path: str):
        self.search_data = search_data
        self.image_dir = image_dir
        print("Initializing IR System")

        print("Building index")
        self.index = Indexing()
        self.index.load_object(object_path)

        print("Initializing retrieval model")
        self.model = {}
        # self.model['vsm'] = VectorSpaceModel(self.index)
        self.model['bm25'] = BM25Model(self.index)
        # self.model['qldps'] = QueryLikelyhoodDPSModel(self.index)

        print("IR System initialized")

    def get_model(self, model_name: str) -> BaseModel:
        return self.model[model_name]

    def search(self, query: str, model: str) -> List[dict]:
        print(f"Searching for '{query}' using {model}")
        results = self.model[model].query_on_index(query)
        results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        tokens = self.index.process_text(query)
        return {
            "tokens": tokens,
            "results": [{"docno": docno, "score": score} for docno, score in results]
        }

    # def get_image(self, filename: str) -> str:
    #     with open(filename, "rb") as f:
    #         image_bytes = io.BytesIO(f.read()).getvalue()
    #         return base64.b64encode(image_bytes).decode('utf-8')
    
    # def get_documents(self, docnos: list) -> List[dict]:
    #     with open(self.search_data, "r", encoding="utf-8") as f:
    #         data = eval(f.read())

    #     results = [data[int(docno)] for docno in docnos]
    #     for result in results:
    #         filename = self.image_dir + str(result['docno']) + ".jpg"
    #         result['image_encoded'] = self.get_image(filename)
    #     return results