import { getImageData } from "./Firestore";

const serverUrl = 'http://127.0.0.1:5000';

const makeGetRequest = async (url) => {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(response);
        }
        return response.json();
    } catch (error) {
        console.error('Error Response:', error);
    }
};


export const initializeAPI = async () => {
    const url = `${serverUrl}/initialize`;
    return await makeGetRequest(url);
};

export const invokeSearchAPI = async ({query, searchModel}) => {
    const params = new URLSearchParams();
    params.append('q', query);
    const url = `${serverUrl}/search/${searchModel}?${params.toString()}`;
    return await makeGetRequest(url);
};

export const fetchDocumentsAPI = async (docnos) => {
    return await getImageData(docnos);
}