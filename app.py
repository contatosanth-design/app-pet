
import React, { useState, useRef } from 'react';
import { GoogleGenAI, Modality } from '@google/genai';
import { encodeAudio, decodeAudio, decodeAudioData } from '../utils/audio';

const LivePanel: React.FC = () => {
  const [isActive, setIsActive] = useState(false);
  const [transcription, setTranscription] = useState<string[]>([]);
  const sessionRef = useRef<any>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const nextStartTimeRef = useRef(0);
  const sourcesRef = useRef<Set<AudioBufferSourceNode>>(new Set());

  const stopSession = () => {
    if (sessionRef.current) {
      sessionRef.current.close();
      sessionRef.current = null;
    }
    setIsActive(false);
    sourcesRef.current.forEach(s => s.stop());
    sourcesRef.current.clear();
  };

  const startSession = async () => {
    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY || '' });
    
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 24000 });
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const inputContext = new AudioContext({ sampleRate: 16000 });
      
      const sessionPromise = ai.live.connect({
        model: 'gemini-2.5-flash-native-audio-preview-12-2025',
        config: {
          responseModalities: [Modality.AUDIO],
          speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: 'Puck' } } },
          inputAudioTranscription: {},
          outputAudioTranscription: {},
          systemInstruction: "Você é Aura, uma assistente virtual de luxo, extremamente inteligente e prestativa. Fale em Português de forma elegante e amigável."
        },
        callbacks: {
          onopen: () => {
            setIsActive(true);
            const source = inputContext.createMediaStreamSource(stream);
            const processor = inputContext.createScriptProcessor(4096, 1, 1);
            processor.onaudioprocess = (e) => {
              const inputData = e.inputBuffer.getChannelData(0);
              const int16 = new Int16Array(inputData.length);
              for (let i = 0; i < inputData.length; i++) int16[i] = inputData[i] * 32768;
              sessionPromise.then(s => s.sendRealtimeInput({ 
                media: { data: encodeAudio(new Uint8Array(int16.buffer)), mimeType: 'audio/pcm;rate=16000' } 
              }));
            };
            source.connect(processor);
            processor.connect(inputContext.destination);
          },
          onmessage: async (msg) => {
            if (msg.serverContent?.modelTurn?.parts?.[0]?.inlineData?.data) {
              const audioData = decodeAudio(msg.serverContent.modelTurn.parts[0].inlineData.data);
              const ctx = audioContextRef.current!;
              nextStartTimeRef.current = Math.max(nextStartTimeRef.current, ctx.currentTime);
              const buffer = await decodeAudioData(audioData, ctx, 24000, 1);
              const source = ctx.createBufferSource();
              source.buffer = buffer;
              source.connect(ctx.destination);
              source.start(nextStartTimeRef.current);
              nextStartTimeRef.current += buffer.duration;
              sourcesRef.current.add(source);
              source.onended = () => sourcesRef.current.delete(source);
            }
            if (msg.serverContent?.outputTranscription) {
               setTranscription(prev => [...prev.slice(-3), `Aura: ${msg.serverContent.outputTranscription.text}`]);
            }
            if (msg.serverContent?.inputTranscription) {
               setTranscription(prev => [...prev.slice(-3), `Você: ${msg.serverContent.inputTranscription.text}`]);
            }
          },
          onclose: () => stopSession(),
          onerror: (e) => {
            console.error("Erro na Live API:", e);
            stopSession();
          }
        }
      });
      sessionRef.current = await sessionPromise;
    } catch (e) {
      console.error(e);
      alert("Erro ao acessar microfone. Verifique as permissões.");
    }
  };

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 bg-slate-900/40 overflow-y-auto custom-scrollbar">
      <div className="max-w-xl w-full text-center space-y-12 py-10">
        <div className="relative flex justify-center">
          <div className={`w-64 h-64 rounded-full flex items-center justify-center transition-all duration-1000 ${isActive ? 'bg-indigo-500/10 scale-110' : 'bg-white/5'}`}>
             <div className={`w-40 h-40 rounded-full flex items-center justify-center transition-all duration-500 ${isActive ? 'bg-indigo-600 shadow-[0_0_50px_rgba(79,70,229,0.4)]' : 'bg-slate-800'}`}>
                <svg className={`w-16 h-16 text-white ${isActive ? 'animate-pulse' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                </svg>
             </div>
             {isActive && [1, 2, 3].map(i => (
               <div key={i} className="absolute inset-0 border border-indigo-500 rounded-full animate-ping opacity-20" style={{ animationDelay: `${i * 0.5}s` }}></div>
             ))}
          </div>
        </div>

        <div className="space-y-4">
          <h2 className="text-4xl font-black text-white">{isActive ? 'Aura está ouvindo...' : 'Aura Live Voice'}</h2>
          <p className="text-slate-400">Experimente uma conversa fluida e natural com IA.</p>
        </div>

        <div className="min-h-[120px] glass-panel p-6 rounded-[2rem] text-sm text-slate-300 text-left space-y-3">
          {transcription.length === 0 ? (
            <p className="text-slate-500 italic text-center">A transcrição aparecerá aqui conforme você fala...</p>
          ) : (
            transcription.map((t, i) => (
              <p key={i} className={t.startsWith('Você:') ? 'text-indigo-400 font-medium' : 'text-slate-300'}>
                {t}
              </p>
            ))
          )}
        </div>

        <button
          onClick={isActive ? stopSession : startSession}
          className={`px-12 py-5 rounded-3xl font-bold text-lg transition-all shadow-xl active:scale-95 ${
            isActive ? 'bg-rose-500 text-white hover:bg-rose-600 shadow-rose-500/20' : 'bg-indigo-600 text-white hover:bg-indigo-500 shadow-indigo-500/20'
          }`}
        >
          {isActive ? 'Encerrar Chamada' : 'Iniciar Conversa'}
        </button>
      </div>
    </div>
  );
};

export default LivePanel;
