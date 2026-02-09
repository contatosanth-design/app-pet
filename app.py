
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
        v3.0 Continuous Voice
      </div>
    </div>
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

  const addTutor = (t: Omit<Tutor, "id">) => {
    setTutores(prev => [...prev, { ...t, id: crypto.randomUUID() }]);
  };

  const addPet = (p: Pet) => {
    setPets(prev => [...prev, p]);
    setActivePetId(p.id);
  };

  const addRecord = (r: Omit<MedicalRecord, "id">) => {
    setRecords(prev => [...prev, { ...r, id: crypto.randomUUID() }]);
  };

  const restoreBackup = (data: any) => {
    if (data.tutores) setTutores(data.tutores);
    if (data.pets) setPets(data.pets);
    if (data.records) setRecords(data.records || data.historico || []);
  };

  const navigateToProntuario = (petId: string) => {
    setActivePetId(petId);
    setCurrentTab(AppTab.PRONTUARIO);
  };

  return (
    <div className="flex min-h-screen">
      <Sidebar currentTab={currentTab} setTab={setCurrentTab} />
      <main className="flex-1 ml-64 p-8 max-w-5xl mx-auto w-full">
        {currentTab === AppTab.TUTORES && (
          <TutorView tutores={tutores} onAdd={addTutor} onGoToPets={() => setCurrentTab(AppTab.PETS)} />
        )}
        {currentTab === AppTab.PETS && (
          <PetView pets={pets} tutores={tutores} onAdd={addPet} onGoToTutores={() => setCurrentTab(AppTab.TUTORES)} onGoToProntuario={navigateToProntuario} />
        )}
        {currentTab === AppTab.PRONTUARIO && (
          <ProntuarioView pets={pets} records={records} onAdd={addRecord} onGoToPets={() => setCurrentTab(AppTab.PETS)} selectedId={activePetId} onSelect={setActivePetId} />
        )}
        {currentTab === AppTab.BACKUP && (
          <BackupView data={{ tutores, pets, records }} onRestore={restoreBackup} />
        )}
      </main>
    </div>
  );
}

// --- Voice Input Component (Updated for Continuous Mode) ---
const VoiceButton: React.FC<{ onResult: (text: string) => void }> = ({ onResult }) => {
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<any>(null);
  
  const toggleListening = () => {
    if (isListening) {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsListening(false);
      return;
    }

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Seu navegador nao suporta reconhecimento de voz.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'pt-BR';
    recognition.continuous = true; // Stay on even after pauses
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onerror = (event: any) => {
      console.error("Erro reconhecimento:", event.error);
      setIsListening(false);
    };
    
    recognition.onresult = (event: any) => {
      // Get the latest result
      const lastIndex = event.results.length - 1;
      const transcript = event.results[lastIndex][0].transcript;
      
      // Only handle final results
      if (event.results[lastIndex].isFinal) {
        onResult(transcript);
      }
    };

    recognitionRef.current = recognition;
    recognition.start();
  };

  return (
    <button
      type="button"
      onClick={toggleListening}
      className={`p-2 rounded-full transition-all flex items-center space-x-2 px-3 ${
        isListening 
        ? 'bg-red-500 text-white shadow-lg shadow-red-200 ring-4 ring-red-100 animate-pulse' 
        : 'bg-slate-100 text-slate-500 hover:bg-blue-100 hover:text-blue-600'
      }`}
      title={isListening ? "Parar Gravacao" : "Iniciar Gravacao Continua"}
    >
      <Icons.Mic />
      {isListening && <span className="text-[10px] font-bold uppercase tracking-widest">Ouvindo...</span>}
    </button>
  );
};

// --- View Components ---
const TutorView: React.FC<{ tutores: Tutor[], onAdd: (t: Omit<Tutor, "id">) => void, onGoToPets: () => void }> = ({ tutores, onAdd, onGoToPets }) => {
  const [form, setForm] = useState({ nome: "", cpf: "", tel: "", email: "", endereco: "" });
  const [justAdded, setJustAdded] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.nome || !form.cpf) return;
    onAdd({ ...form, nome: form.nome.toUpperCase() });
    setForm({ nome: "", cpf: "", tel: "", email: "", endereco: "" });
    setJustAdded(true);
    setTimeout(() => setJustAdded(false), 8000);
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      <header>
        <h2 className="text-3xl font-bold text-slate-800">Cadastro de Tutores</h2>
        <p className="text-slate-500 font-medium">Gerencie os proprietarios dos pacientes.</p>
      </header>
      {justAdded && (
        <div className="bg-green-50 border border-green-200 text-green-800 p-4 rounded-2xl flex justify-between items-center shadow-sm">
          <div className="flex items-center space-x-2">
            <span className="text-green-600"><Icons.Check /></span>
            <span className="font-semibold">Tutor salvo. Vamos cadastrar o Pet?</span>
          </div>
          <button onClick={onGoToPets} className="bg-green-600 text-white px-4 py-2 rounded-xl font-bold text-sm hover:bg-green-700 transition-colors flex items-center space-x-2">
            <span>CADASTRAR PET</span>
            <Icons.ArrowRight />
          </button>
        </div>
      )}
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div><label className="block text-xs font-bold text-slate-400 uppercase mb-2">Nome do Tutor *</label><input type="text" required className="w-full px-4 py-3 bg-slate-50 border rounded-xl focus:bg-white outline-none" value={form.nome} onChange={e => setForm({ ...form, nome: e.target.value })} placeholder="EX: JOAO DA SILVA" /></div>
          <div><label className="block text-xs font-bold text-slate-400 uppercase mb-2">CPF *</label><input type="text" required className="w-full px-4 py-3 bg-slate-50 border rounded-xl focus:bg-white outline-none" value={form.cpf} onChange={e => setForm({ ...form, cpf: e.target.value })} placeholder="000.000.000-00" /></div>
          <div><label className="block text-xs font-bold text-slate-400 uppercase mb-2">WhatsApp</label><input type="text" className="w-full px-4 py-3 bg-slate-50 border rounded-xl focus:bg-white outline-none" value={form.tel} onChange={e => setForm({ ...form, tel: e.target.value })} placeholder="(00) 00000-0000" /></div>
          <div><label className="block text-xs font-bold text-slate-400 uppercase mb-2">E-mail</label><input type="email" className="w-full px-4 py-3 bg-slate-50 border rounded-xl focus:bg-white outline-none" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} placeholder="email@exemplo.com" /></div>
          <div className="md:col-span-2"><label className="block text-xs font-bold text-slate-400 uppercase mb-2">Endereco</label><input type="text" className="w-full px-4 py-3 bg-slate-50 border rounded-xl focus:bg-white outline-none" value={form.endereco} onChange={e => setForm({ ...form, endereco: e.target.value })} placeholder="Rua, numero, bairro..." /></div>
        </div>
        <button type="submit" className="w-full bg-blue-600 text-white py-4 rounded-2xl font-bold hover:bg-blue-700 transition shadow-xl"><span>SALVAR TUTOR</span></button>
      </form>
    </div>
  );
};

const PetView: React.FC<{ pets: Pet[], tutores: Tutor[], onAdd: (p: Pet) => void, onGoToTutores: () => void, onGoToProntuario: (id: string) => void }> = ({ pets, tutores, onAdd, onGoToTutores, onGoToProntuario }) => {
  const [form, setForm] = useState({ nome: "", raca: "", nascimento: "", tutorId: "" });
  const [newPetId, setNewPetId] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.nome || !form.tutorId) return;
    const generatedId = crypto.randomUUID();
    onAdd({ ...form, id: generatedId, nome: form.nome.toUpperCase(), raca: form.raca.toUpperCase() });
    setForm({ nome: "", raca: "", nascimento: "", tutorId: "" });
    setNewPetId(generatedId);
  };

  if (tutores.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center space-y-6 py-24 bg-white rounded-3xl border text-center">
        <Icons.Warning /><h3 className="text-xl font-bold">Nenhum Tutor Cadastrado</h3><button onClick={onGoToTutores} className="bg-blue-600 text-white px-8 py-3 rounded-xl font-bold">CADASTRAR TUTOR AGORA</button>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fadeIn">
      <header><h2 className="text-3xl font-bold text-slate-800">Cadastro de Pacientes</h2><p className="text-slate-500 font-medium">Registre os pets e vincule aos proprietarios.</p></header>
      {newPetId && (
        <div className="bg-blue-50 border border-blue-100 p-5 rounded-3xl flex justify-between items-center shadow-sm animate-fadeIn">
          <div className="flex items-center space-x-3 text-blue-900 font-bold"><span className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center"><Icons.Check /></span><span>Paciente salvo. Abrir prontuario agora?</span></div>
          <button onClick={() => onGoToProntuario(newPetId)} className="bg-blue-600 text-white px-6 py-2.5 rounded-2xl font-bold hover:bg-blue-700 flex items-center space-x-2"><span>ABRIR PRONTUARIO</span><Icons.Record /></button>
        </div>
      )}
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="md:col-span-2"><label className="block text-xs font-bold text-slate-400 uppercase mb-2">Selecione o Tutor *</label><select required className="w-full px-4 py-3 bg-slate-50 border rounded-xl focus:bg-white outline-none cursor-pointer" value={form.tutorId} onChange={e => setForm({ ...form, tutorId: e.target.value })}><option value="">--- Selecionar proprietario ---</option>{tutores.map(t => (<option key={t.id} value={t.id}>{t.nome} (CPF: {t.cpf})</option>))}</select></div>
          <div><label className="block text-xs font-bold text-slate-400 uppercase mb-2">Nome do Pet *</label><input type="text" required className="w-full px-4 py-3 bg-slate-50 border rounded-xl focus:bg-white outline-none" value={form.nome} onChange={e => setForm({ ...form, nome: e.target.value })} placeholder="EX: LUNA" /></div>
          <div><label className="block text-xs font-bold text-slate-400 uppercase mb-2">Raca</label><input type="text" className="w-full px-4 py-3 bg-slate-50 border rounded-xl focus:bg-white outline-none" value={form.raca} onChange={e => setForm({ ...form, raca: e.target.value })} placeholder="EX: BORDER COLLIE" /></div>
          <div><label className="block text-xs font-bold text-slate-400 uppercase mb-2">Nascimento</label><input type="text" className="w-full px-4 py-3 bg-slate-50 border rounded-xl focus:bg-white outline-none" value={form.nascimento} onChange={e => setForm({ ...form, nascimento: e.target.value })} placeholder="DD/MM/AAAA" /></div>
        </div>
        <button type="submit" className="w-full bg-blue-600 text-white py-4 rounded-2xl font-bold shadow-lg shadow-blue-50">SALVAR PACIENTE</button>
      </form>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">{pets.map(p => (<div key={p.id} className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm flex flex-col justify-between group hover:shadow-md transition-all"><div className="flex items-start space-x-4"><div className="w-12 h-12 bg-blue-50 text-blue-500 rounded-2xl flex items-center justify-center group-hover:bg-blue-600 group-hover:text-white transition-all"><Icons.Pet /></div><div><h4 className="font-bold text-slate-800">{p.nome}</h4><p className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">{p.raca || "N/A"}</p></div></div><div className="mt-4 flex justify-between items-center pt-4 border-t border-slate-50"><div className="text-xs text-slate-600 font-medium">{tutores.find(t => t.id === p.tutorId)?.nome}</div><button onClick={() => onGoToProntuario(p.id)} className="text-blue-600 hover:text-blue-800"><Icons.Record /></button></div></div>))}</div>
    </div>
  );
};

const ProntuarioView: React.FC<{ pets: Pet[], records: MedicalRecord[], onAdd: (r: Omit<MedicalRecord, "id">) => void, onGoToPets: () => void, selectedId: string, onSelect: (id: string) => void }> = ({ pets, records, onAdd, onGoToPets, selectedId, onSelect }) => {
  const [sintomas, setSintomas] = useState("");
  const [observacoes, setObservacoes] = useState("");
  const [isAiLoading, setIsAiLoading] = useState(false);
  const [aiSuggestion, setAiSuggestion] = useState("");

  const selectedPet = pets.find(p => p.id === selectedId);

  const handleAiConsult = async () => {
    if (!sintomas || !selectedPet) return;
    setIsAiLoading(true);
    const suggestion = await getAiDiagnosisSuggestion(sintomas, { nome: selectedPet.nome, raca: selectedPet.raca });
    setAiSuggestion(suggestion || "");
    setIsAiLoading(false);
  };

  const handleVoiceResult = (field: 'sintomas' | 'observacoes', text: string) => {
    if (field === 'sintomas') {
      setSintomas(prev => prev ? `${prev} ${text}` : text);
    } else {
      setObservacoes(prev => prev ? `${prev} ${text}` : text);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedId) return;
    onAdd({ petId: selectedId, data: new Date().toLocaleDateString("pt-BR"), observacoes, sintomas, diagnosticoAi: aiSuggestion });
    setSintomas(""); setObservacoes(""); setAiSuggestion("");
    alert("Consulta registrada!");
  };

  if (pets.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center space-y-6 py-24 bg-white rounded-3xl border text-center">
        <Icons.Record /><h3 className="text-xl font-bold">Sem Pacientes Cadastrados</h3><button onClick={onGoToPets} className="bg-blue-600 text-white px-8 py-3 rounded-xl font-bold shadow-lg">CADASTRAR PET AGORA</button>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fadeIn pb-24">
      <header><h2 className="text-3xl font-bold text-slate-800">Prontuario Medico</h2><p className="text-slate-500 font-medium">Historico de consultas e IA veterinaria.</p></header>
      <div className="bg-white p-8 rounded-[32px] shadow-sm border border-slate-100 space-y-8">
        <div><label className="block text-xs font-bold text-slate-400 uppercase mb-3">Paciente Ativo</label><select className="w-full px-5 py-4 bg-slate-50 border rounded-2xl outline-none text-lg font-bold text-slate-700 cursor-pointer" value={selectedId} onChange={e => { onSelect(e.target.value); setAiSuggestion(""); }}><option value="">--- Selecionar Paciente ---</option>{pets.map(p => (<option key={p.id} value={p.id}>{p.nome} ({p.raca})</option>))}</select></div>
        {selectedId && (
          <div className="space-y-8 animate-fadeIn">
            <div className="space-y-4">
              <div className="flex justify-between items-center"><label className="block text-xs font-bold text-slate-400 uppercase">Sintomas (Gravacao Continua Ativada)</label><VoiceButton onResult={(text) => handleVoiceResult('sintomas', text)} /></div>
              <textarea className="w-full px-5 py-4 bg-slate-50 border rounded-2xl outline-none min-h-[120px]" placeholder="Dite ou escreva os sintomas..." value={sintomas} onChange={e => setSintomas(e.target.value)} />
              <button type="button" onClick={handleAiConsult} disabled={isAiLoading || !sintomas} className="flex items-center space-x-3 px-6 py-3 bg-blue-50 text-blue-700 rounded-2xl font-bold hover:bg-blue-100 transition-all disabled:opacity-50"><span className={isAiLoading ? "animate-spin" : ""}><Icons.Sparkles /></span><span>{isAiLoading ? "Analisando..." : "Consultar Diagnostico IA"}</span></button>
            </div>
            {aiSuggestion && (<div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-3xl text-white shadow-xl animate-slideUp"><div className="flex items-center space-x-2 mb-4"><Icons.AI /> <h4 className="font-bold">Analise Pro IA</h4></div><div className="text-sm whitespace-pre-wrap opacity-95 leading-relaxed">{aiSuggestion}</div></div>)}
            <div className="space-y-4">
              <div className="flex justify-between items-center"><label className="block text-xs font-bold text-slate-400 uppercase">Conduta Veterinaria</label><VoiceButton onResult={(text) => handleVoiceResult('observacoes', text)} /></div>
              <textarea className="w-full px-5 py-4 bg-slate-50 border rounded-2xl outline-none min-h-[100px]" placeholder="Dite a conduta e medicamentos..." value={observacoes} onChange={e => setObservacoes(e.target.value)} />
            </div>
            <button onClick={handleSubmit} className="w-full bg-slate-900 text-white py-5 rounded-2xl font-bold uppercase text-sm hover:bg-black shadow-xl">Salvar Consulta</button>
          </div>
        )}
      </div>
      <div className="space-y-6"><h3 className="text-xl font-bold text-slate-800 px-2 flex items-center space-x-2"><Icons.Record /><span>Historico do Paciente</span></h3><div className="space-y-4">{records.filter(r => r.petId === selectedId).reverse().map(r => (<div key={r.id} className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm"><div className="flex justify-between items-center mb-4"><span className="bg-blue-50 text-blue-600 px-3 py-1 rounded-full text-xs font-bold">{r.data}</span></div><div className="grid grid-cols-1 md:grid-cols-2 gap-4"><div><h5 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Anamnese</h5><p className="text-sm text-slate-700">{r.sintomas}</p></div><div><h5 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Conduta</h5><p className="text-sm text-slate-700">{r.observacoes}</p></div></div></div>))}</div></div>
    </div>
  );
};

const BackupView: React.FC<{ data: any, onRestore: (data: any) => void }> = ({ data, onRestore }) => {
  const downloadBackup = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = "backup_ribeira_vet.json"; a.click(); URL.revokeObjectURL(url);
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]; if (!file) return;
    const reader = new FileReader(); reader.onload = (event) => {
      try { onRestore(JSON.parse(event.target?.result as string)); alert("Dados restaurados!"); } catch (err) { alert("Erro no arquivo."); }
    }; reader.readAsText(file);
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      <header><h2 className="text-3xl font-bold text-slate-800">Seguranca e Backup</h2><p className="text-slate-500 font-medium">Exportar ou restaurar base de dados local.</p></header>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8"><div className="bg-white p-10 rounded-[40px] border shadow-sm flex flex-col items-center space-y-6 group hover:shadow-lg transition-all"><div className="w-16 h-16 bg-green-50 text-green-500 rounded-2xl flex items-center justify-center text-3xl group-hover:scale-110"><Icons.Backup /></div><h3 className="text-xl font-bold text-slate-800">Exportar Base</h3><button onClick={downloadBackup} className="w-full bg-green-600 text-white py-4 rounded-2xl font-bold shadow-lg">GERAR BACKUP</button></div><div className="bg-white p-10 rounded-[40px] border shadow-sm flex flex-col items-center space-y-6 group hover:shadow-lg transition-all"><div className="w-16 h-16 bg-amber-50 text-amber-500 rounded-2xl flex items-center justify-center text-3xl group-hover:scale-110"><Icons.Warning /></div><h3 className="text-xl font-bold text-slate-800">Restaurar Base</h3><div className="w-full relative"><input type="file" accept=".json" onChange={handleFileUpload} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" /><div className="bg-amber-600 text-white py-4 rounded-2xl font-bold text-center shadow-lg">SUBIR ARQUIVO</div></div></div></div>
    </div>
  );
};
