// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore, collection, query, where, getDocs } from "firebase/firestore";
import { getStorage, ref, getDownloadURL } from "firebase/storage";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

const IMAGE_DATA_COLLECTION = "image-data";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "",
    authDomain: "",
    projectId: "",
    storageBucket: "",
    messagingSenderId: "",
    appId: ""
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

const db = getFirestore(app, 'xxxxxx-xxxxxx');
const storage = getStorage(app, 'gs://xxxxx-xxxxx-xxxxxx');

export const getImageData = async (docnos) => {
    const q = query(collection(db, IMAGE_DATA_COLLECTION), where('docno', 'in', docnos));
    const querySnapshot = await getDocs(q);
    const docs = querySnapshot.docs.map(doc => doc.data());

    // Createing new promises for getting image urls
    const promises = docs.map(doc => getImageUrl(doc.docno));
    const urls = await Promise.all(promises);

    // Updating the docs with image urls
    docs.forEach((doc, index) => {
        doc.static_link = urls[index];
    });
    
    return docs;
};

export const getImageUrl = (docno) => {
    const pathReference = ref(storage, `images/${docno}.jpg`);
    return getDownloadURL(pathReference);
};