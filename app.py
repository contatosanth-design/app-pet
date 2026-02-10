
import { GoogleGenAI } from "@google/genai";

const getAI = () => new GoogleGenAI({ apiKey: process.env.API_KEY || '' });

export const creativeChat = async (prompt: string, useThinking: boolean = false) => {
  const ai = getAI();
  const modelName = useThinking ? 'gemini-3-pro-preview' : 'gemini-3-flash-preview';
  
  const config: any = {
    temperature: 0.8,
    topP: 0.9,
  };

  if (useThinking) {
    config.thinkingConfig = { thinkingBudget: 16000 };
  }

  return await ai.models.generateContent({
    model: modelName,
    contents: prompt,
    config,
  });
};

export const generateArt = async (prompt: string, aspectRatio: string = "1:1") => {
  const ai = getAI();
  const response = await ai.models.generateContent({
    model: 'gemini-2.5-flash-image',
    contents: { parts: [{ text: prompt }] },
    config: { imageConfig: { aspectRatio: aspectRatio as any } }
  });

  for (const part of response.candidates?.[0]?.content?.parts || []) {
    if (part.inlineData) return `data:image/png;base64,${part.inlineData.data}`;
  }
  throw new Error("No image data returned from Gemini.");
};

export const generateVideo = async (prompt: string) => {
  const ai = getAI();
  let operation = await ai.models.generateVideos({
    model: 'veo-3.1-fast-generate-preview',
    prompt: prompt,
    config: {
      numberOfVideos: 1,
      resolution: '720p',
      aspectRatio: '16:9'
    }
  });

  while (!operation.done) {
    await new Promise(resolve => setTimeout(resolve, 5000));
    operation = await ai.operations.getVideosOperation({ operation: operation });
  }

  const downloadLink = operation.response?.generatedVideos?.[0]?.video?.uri;
  const response = await fetch(`${downloadLink}&key=${process.env.API_KEY}`);
  const blob = await response.blob();
  return URL.createObjectURL(blob);
};

export const mapsSearch = async (query: string, location?: { latitude: number, longitude: number }) => {
  const ai = getAI();
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: query,
    config: {
      tools: [{ googleMaps: {} }, { googleSearch: {} }],
      toolConfig: {
        retrievalConfig: {
          latLng: location ? {
            latitude: location.latitude,
            longitude: location.longitude
          } : undefined
        }
      }
    },
  });

  return {
    text: response.text,
    grounding: response.candidates?.[0]?.groundingMetadata?.groundingChunks || []
  };
};
