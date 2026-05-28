import apiClient from "../../../services/apiClient";

export const askAI = async (question, files = []) => {

    const payload = { question };

    if (files && files.length) payload.files = files;

    const response = await apiClient.post(

        "/api/chat/",

        payload
    );

    return response.data;
};