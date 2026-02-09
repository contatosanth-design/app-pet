
import React, { useState, useEffect, useRef } from 'react';
import { Tutor, Pet, MedicalRecord, AppTab } from './types';
import { getAiDiagnosisSuggestion } from './services/geminiService';

// --- SVG Icons ---
const Icons = {
  Tutor: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>,
  Pet: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>,
  Record: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>,
  Backup: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" /></svg>,
  AI: () => <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 10-2 0v1a1 1 0 102 0v-1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 10-2 0v1a1 1 0 102 0v-1zM8 16v-1a1 1 0 10-2 0v1a1 1 0 102 0zM12 16v-1a1 1 0 10-2 0v1a1 1 0 102 0zM16 16v-1a1 1 0 10-2 0v1a1 1 0 102 0z" /></svg>,
  Check: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" /></svg>,
  Warning: () => <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>,
  ArrowRight: () => <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>,
  Sparkles: () => <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" /></svg>,
  Mic: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 10v2a7 7 0 01-14 0v-2m7 9v3m-3 0h6" /></svg>
};

// --- Sidebar ---
const Sidebar: React.FC<{ currentTab: AppTab; setTab: (tab: AppTab) => void }> = ({ currentTab, setTab }) => {
  const menuItems = [
    { id: AppTab.TUTORES, icon: <Icons.Tutor />, label: "Tutores" },
    { id: AppTab.PETS, icon: <Icons.Pet />, label: "Pets" },
    { id: AppTab.PRONTUARIO, icon: <Icons.Record />, label: "Prontuario" },
    { id: AppTab.BACKUP, icon: <Icons.Backup />, label: "Backup" },
  ];

  return (
    <div className="w-64 bg-white border-r h-screen flex flex-col fixed left-0 top-0 z-10">
      <div className="p-6 border-b flex items-center space-x-2">
        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">RV</div>
        <h1 className="text-xl font-bold text-slate-800">Ribeira Vet</h1>
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setTab(item.id)}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 ${
              currentTab === item.id
                ? "bg-blue-600 text-white shadow-lg shadow-blue-200"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            {item.icon}
            <span className="font-semibold">{item.label}</span>
          </button>
        ))}
      </nav>
      <div className="p-4 border-t text-[10px] text-slate-400 text-center uppercase tracking-widest font-bold">
        v3.1 Pro Voice AI
      </div>
    </div>
  );
};

// --- Voice Input Component (Enhanced Continuous Mode) ---
const VoiceButton: React.FC<{ onResult: (text: string) => void }> = ({ onResult }) => {
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<any>(null);
  const shouldRestartRef = useRef(false);

  const initRecognition = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) return null;

    const recognition = new SpeechRecognition();
    recognition.lang = 'pt-BR';
    recognition.continuous = true;
    recognition.interimResults = false;

    recognition.onstart = () => {
      setIsListening(true);
      shouldRestartRef.current = true;
    };

    recognition.onend = () => {
      // Se o sistema desligar sozinho por silêncio mas o estado "shouldRestart" for true, religamos.
      if (shouldRestartRef.current) {
        recognition.start();
      } else {
        setIsListening(false);
      }
    };

    recognition.onerror = (event: any) => {
      console.error("Erro voz:", event.error);
      if (event.error === 'no-speech') return; // Ignora se for apenas silêncio
      shouldRestartRef.current = false;
      setIsListening(false);
    };

    recognition.onresult = (event: any) => {
      const lastIndex = event.results.length - 1;
      const transcript = event.results[lastIndex][0].transcript;
      if (event.results[lastIndex].isFinal) {
        onResult(transcript);
      }
    };

    return recognition;
  };

  const toggleListening = () => {
    if (isListening) {
      shouldRestartRef.current = false;
      if (recognitionRef.current) recognitionRef.current.stop();
      setIsListening(false);
    } else {
      const rec = initRecognition();
      if (rec) {
        recognitionRef.current = rec;
        rec.start();
      } else {
        alert("Reconhecimento de voz não suportado neste navegador.");
      }
    }
  };

  return (
    <button
      type="button"
      onClick={toggleListening}
      className={`p-2 rounded-full transition-all flex items-center space-x-2 px-3 ${
        isListening 
        ? 'bg-red-600 text-white shadow-lg ring-4 ring-red-100 animate-pulse' 
        : 'bg-slate-100 text-slate-500 hover:bg-blue-100 hover:text-blue-600'
      }`}
    >
      <Icons.Mic />
      {isListening && <span className="text-[10px] font-bold uppercase">Gravando...</span>}
    </button>
  );
};

export default function App() {
  const [currentTab, setCurrentTab] = useState<AppTab>(AppTab.TUTORES);
  const [tutores, setTutores] = useState<Tutor[]>([]);
  const [pets, setPets] = useState<Pet[]>([]);
  const [records, setRecords] = useState<MedicalRecord[]>([]);
  const [activePetId, setActivePetId] = useState<string>("");

  useEffect(() => {
    const savedTutores = localStorage.getItem("rv_tutores");
    const savedPets = localStorage.getItem("rv_pets");
    const savedRecords = localStorage.getItem("rv_records");
    if (savedTutores) setTutores(JSON.parse(savedTutores));
    if (savedPets) setPets(JSON.parse(savedPets));
    if (savedRecords) setRecords(JSON.parse(savedRecords));
  }, []);

  useEffect(() => {
    localStorage.setItem("rv_tutores", JSON.stringify(tutores));
    localStorage.setItem("rv_pets", JSON.stringify(pets));
    localStorage.setItem("rv_records", JSON.stringify(records));
  }, [tutores, pets, records]);

  const addTutor = (t: Omit<Tutor, "id">) => setTutores(prev => [...prev, { ...t, id: crypto.randomUUID() }]);
  const addPet = (p: Pet) => { setPets(prev => [...prev, p]); setActivePetId(p.id); };
  const addRecord = (r: Omit<MedicalRecord, "id">) => setRecords(prev => [...prev, { ...r, id: crypto.randomUUID() }]);
  const restoreBackup = (data: any) => {
    setTutores(data.tutores || []);
    setPets(data.pets || []);
    setRecords(data.records || data.historico || []);
  };

  return (
    <div className="flex min-h-screen">
      <Sidebar currentTab={currentTab} setTab={setCurrentTab} />
      <main className="flex-1 ml-64 p-8 max-w-5xl mx-auto w-full">
        {currentTab === AppTab.TUTORES && <TutorView tutores={tutores} onAdd={addTutor} onGoToPets={() => setCurrentTab(AppTab.PETS)} />}
        {currentTab === AppTab.PETS && <PetView pets={pets} tutores={tutores} onAdd={addPet} onGoToTutores={() => setCurrentTab(AppTab.TUTORES)} onGoToProntuario={(id) => { setActivePetId(id); setCurrentTab(AppTab.PRONTUARIO); }} />}
        {currentTab === AppTab.PRONTUARIO && <ProntuarioView pets={pets} records={records} onAdd={addRecord} onGoToPets={() => setCurrentTab(AppTab.PETS)} selectedId={activePetId} onSelect={setActivePetId} />}
        {currentTab === AppTab.BACKUP && <BackupView data={{ tutores, pets, records }} onRestore={restoreBackup} />}
      </main>
    </div>
  );
}

// --- Views ---

const TutorView: React.FC<{ tutores: Tutor[], onAdd: (t: Omit<Tutor, "id">) => void, onGoToPets: () => void }> = ({ tutores, onAdd, onGoToPets }) => {
  const [form, setForm] = useState({ nome: "", cpf: "", tel: "", email: "", endereco: "" });
  const [added, setAdded] = useState(false);

  const sub = (e: React.FormEvent) => {
    e.preventDefault();
    onAdd({ ...form, nome: form.nome.toUpperCase() });
    setForm({ nome: "", cpf: "", tel: "", email: "", endereco: "" });
    setAdded(true);
    setTimeout(() => setAdded(false), 5000);
  };

  return (
    <div className="space-y-8">
      <header><h2 className="text-3xl font-bold">Tutores</h2><p className="text-slate-500">Cadastre o proprietário antes do pet.</p></header>
      {added && <div className="bg-green-50 p-4 rounded-xl flex justify-between items-center border border-green-200"><span>Tutor salvo com sucesso!</span><button onClick={onGoToPets} className="bg-green-600 text-white px-4 py-2 rounded-lg font-bold">CADASTRAR PET</button></div>}
      <form onSubmit={sub} className="bg-white p-8 rounded-3xl shadow-sm border space-y-4">
        <input placeholder="NOME DO TUTOR *" required className="w-full p-4 bg-slate-50 rounded-xl" value={form.nome} onChange={e => setForm({...form, nome: e.target.value})} />
        <input placeholder="CPF *" required className="w-full p-4 bg-slate-50 rounded-xl" value={form.cpf} onChange={e => setForm({...form, cpf: e.target.value})} />
        <div className="grid grid-cols-2 gap-4">
          <input placeholder="WhatsApp" className="p-4 bg-slate-50 rounded-xl" value={form.tel} onChange={e => setForm({...form, tel: e.target.value})} />
          <input placeholder="E-mail" className="p-4 bg-slate-50 rounded-xl" value={form.email} onChange={e => setForm({...form, email: e.target.value})} />
        </div>
        <button className="w-full bg-blue-600 text-white py-4 rounded-xl font-bold shadow-lg">SALVAR TUTOR</button>
      </form>
    </div>
  );
};

const PetView: React.FC<{ pets: Pet[], tutores: Tutor[], onAdd: (p: Pet) => void, onGoToTutores: () => void, onGoToProntuario: (id: string) => void }> = ({ pets, tutores, onAdd, onGoToTutores, onGoToProntuario }) => {
  const [form, setForm] = useState({ nome: "", raca: "", nascimento: "", tutorId: "" });
  
  if (tutores.length === 0) return <div className="p-12 text-center bg-white rounded-3xl border"><h3>Cadastre um Tutor primeiro.</h3><button onClick={onGoToTutores} className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg">Ir para Tutores</button></div>;

  return (
    <div className="space-y-8">
      <header><h2 className="text-3xl font-bold">Pacientes</h2></header>
      <form onSubmit={(e) => { e.preventDefault(); onAdd({...form, id: crypto.randomUUID()}); setForm({nome:"", raca:"", nascimento:"", tutorId:""}); }} className="bg-white p-8 rounded-3xl border space-y-4 shadow-sm">
        <select required className="w-full p-4 bg-slate-50 rounded-xl" value={form.tutorId} onChange={e => setForm({...form, tutorId: e.target.value})}>
          <option value="">--- Selecionar Tutor ---</option>
          {tutores.map(t => <option key={t.id} value={t.id}>{t.nome}</option>)}
        </select>
        <div className="grid grid-cols-2 gap-4">
          <input placeholder="Nome do Pet" required className="p-4 bg-slate-50 rounded-xl" value={form.nome} onChange={e => setForm({...form, nome: e.target.value})} />
          <input placeholder="Raça" className="p-4 bg-slate-50 rounded-xl" value={form.raca} onChange={e => setForm({...form, raca: e.target.value})} />
        </div>
        <button className="w-full bg-blue-600 text-white py-4 rounded-xl font-bold">SALVAR PET</button>
      </form>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {pets.map(p => (
          <div key={p.id} className="bg-white p-6 rounded-3xl border hover:shadow-md transition-all flex justify-between items-center">
            <div><h4 className="font-bold">{p.nome}</h4><p className="text-xs text-slate-400">{p.raca}</p></div>
            <button onClick={() => onGoToProntuario(p.id)} className="text-blue-600"><Icons.Record /></button>
          </div>
        ))}
      </div>
    </div>
  );
};

const ProntuarioView: React.FC<{ pets: Pet[], records: MedicalRecord[], onAdd: (r: Omit<MedicalRecord, "id">) => void, onGoToPets: () => void, selectedId: string, onSelect: (id: string) => void }> = ({ pets, records, onAdd, onGoToPets, selectedId, onSelect }) => {
  const [sin, setSin] = useState("");
  const [obs, setObs] = useState("");
  const [loading, setLoading] = useState(false);
  const [ai, setAi] = useState("");

  const selectedPet = pets.find(p => p.id === selectedId);

  const askAi = async () => {
    if (!sin || !selectedPet) return;
    setLoading(true);
    const res = await getAiDiagnosisSuggestion(sin, { nome: selectedPet.nome, raca: selectedPet.raca });
    setAi(res || "");
    setLoading(false);
  };

  const handleVoice = (field: 'sin' | 'obs', text: string) => {
    if (field === 'sin') setSin(prev => prev ? `${prev} ${text}` : text);
    else setObs(prev => prev ? `${prev} ${text}` : text);
  };

  return (
    <div className="space-y-8 pb-24">
      <header><h2 className="text-3xl font-bold text-slate-800">Prontuário</h2></header>
      <div className="bg-white p-8 rounded-[32px] border shadow-sm space-y-6">
        <select className="w-full p-4 bg-slate-50 rounded-2xl font-bold text-lg" value={selectedId} onChange={e => { onSelect(e.target.value); setAi(""); }}>
          <option value="">--- Selecionar Paciente ---</option>
          {pets.map(p => <option key={p.id} value={p.id}>{p.nome} ({p.raca})</option>)}
        </select>

        {selectedId && (
          <div className="space-y-6">
            <div>
              <div className="flex justify-between items-center mb-2"><label className="text-xs font-bold text-slate-400 uppercase">Sintomas / Anamnese</label><VoiceButton onResult={(t) => handleVoice('sin', t)} /></div>
              <textarea className="w-full p-5 bg-slate-50 rounded-2xl min-h-[120px]" placeholder="Relate o que o pet apresenta..." value={sin} onChange={e => setSin(e.target.value)} />
              <button onClick={askAi} disabled={loading || !sin} className="mt-3 flex items-center space-x-2 bg-blue-50 text-blue-700 px-6 py-2 rounded-xl font-bold">
                <Icons.Sparkles /> <span>{loading ? "Processando..." : "Consultar Inteligência Artificial"}</span>
              </button>
            </div>

            {ai && <div className="bg-blue-600 p-6 rounded-3xl text-white text-sm shadow-xl whitespace-pre-wrap leading-relaxed"><div className="flex items-center space-x-2 mb-2 font-bold"><Icons.AI /><span>Sugestão Clínica Pro AI</span></div>{ai}</div>}

            <div>
              <div className="flex justify-between items-center mb-2"><label className="text-xs font-bold text-slate-400 uppercase">Conduta / Receituário</label><VoiceButton onResult={(t) => handleVoice('obs', t)} /></div>
              <textarea className="w-full p-5 bg-slate-50 rounded-2xl min-h-[100px]" placeholder="Prescrições e orientações..." value={obs} onChange={e => setObs(e.target.value)} />
            </div>

            <button onClick={() => { onAdd({ petId: selectedId, data: new Date().toLocaleDateString("pt-BR"), observacoes: obs, sintomas: sin, diagnosticoAi: ai }); setSin(""); setObs(""); setAi(""); alert("Salvo!"); }} className="w-full bg-slate-900 text-white py-4 rounded-xl font-bold uppercase shadow-xl">Finalizar Atendimento</button>
          </div>
        )}
      </div>

      <div className="space-y-4">
        <h3 className="font-bold">Histórico do Paciente</h3>
        {records.filter(r => r.petId === selectedId).reverse().map(r => (
          <div key={r.id} className="bg-white p-6 rounded-3xl border">
            <span className="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded mb-2 inline-block">{r.data}</span>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div><p className="font-bold text-slate-400 uppercase text-[10px]">Anamnese</p><p>{r.sintomas}</p></div>
              <div><p className="font-bold text-slate-400 uppercase text-[10px]">Conduta</p><p>{r.observacoes}</p></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const BackupView: React.FC<{ data: any, onRestore: (d: any) => void }> = ({ data, onRestore }) => (
  <div className="space-y-8">
    <header><h2 className="text-3xl font-bold">Backup</h2></header>
    <div className="grid grid-cols-2 gap-8">
      <button onClick={() => { const blob = new Blob([JSON.stringify(data)], {type:"application/json"}); const url = URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = "ribeira_vet_data.json"; a.click(); }} className="bg-white p-12 rounded-[40px] border shadow-sm flex flex-col items-center space-y-4 group">
        <div className="w-16 h-16 bg-green-50 text-green-600 rounded-2xl flex items-center justify-center group-hover:scale-110 transition"><Icons.Backup /></div>
        <span className="font-bold">Baixar Base de Dados</span>
      </button>
      <div className="relative bg-white p-12 rounded-[40px] border shadow-sm flex flex-col items-center space-y-4 group cursor-pointer">
        <input type="file" className="absolute inset-0 opacity-0 cursor-pointer" onChange={(e) => { const f = e.target.files?.[0]; if(!f) return; const r = new FileReader(); r.onload=(ev) => { try { onRestore(JSON.parse(ev.target?.result as string)); alert("Restaurado!"); } catch { alert("Erro"); } }; r.readAsText(f); }} />
        <div className="w-16 h-16 bg-amber-50 text-amber-600 rounded-2xl flex items-center justify-center group-hover:scale-110 transition"><Icons.Warning /></div>
        <span className="font-bold">Restaurar do Arquivo</span>
      </div>
    </div>
  </div>
);
