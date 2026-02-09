
import React, { useState, useEffect, useRef } from 'react';
import { Tutor, Pet, MedicalRecord, AppTab } from './types';
import { getAiDiagnosisSuggestion } from './services/geminiService';

// --- Ícones de Alta Definição ---
const Icons = {
  Tutor: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>,
  Pet: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>,
  Record: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>,
  Backup: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" /></svg>,
  AI: () => <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 10-2 0v1a1 1 0 102 0v-1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 10-2 0v1a1 1 0 102 0v-1zM8 16v-1a1 1 0 10-2 0v1a1 1 0 102 0zM12 16v-1a1 1 0 10-2 0v1a1 1 0 102 0zM16 16v-1a1 1 0 10-2 0v1a1 1 0 102 0z" /></svg>,
  Mic: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 10v2a7 7 0 01-14 0v-2m7 9v3m-3 0h6" /></svg>,
  Sparkles: () => <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" /></svg>,
  Warning: () => <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
};

// --- Botão de Voz Profissional (Não desliga sozinho) ---
const VoiceButton: React.FC<{ onResult: (text: string) => void }> = ({ onResult }) => {
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<any>(null);
  const shouldBeListeningRef = useRef(false);

  const startRecognition = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Seu navegador não suporta reconhecimento de voz.");
      return;
    }

    const rec = new SpeechRecognition();
    rec.lang = 'pt-BR';
    rec.continuous = true;
    rec.interimResults = false;

    rec.onstart = () => {
      setIsListening(true);
      shouldBeListeningRef.current = true;
    };

    rec.onend = () => {
      // O segredo do religamento: se o sistema fechou mas nós queremos continuar, iniciamos de novo.
      if (shouldBeListeningRef.current) {
        try {
          rec.start();
        } catch (e) {
          console.log("Reiniciando captura...");
        }
      } else {
        setIsListening(false);
      }
    };

    rec.onresult = (event: any) => {
      const lastIndex = event.results.length - 1;
      const transcript = event.results[lastIndex][0].transcript;
      if (event.results[lastIndex].isFinal) {
        onResult(transcript);
      }
    };

    rec.onerror = (event: any) => {
      // Erro de silêncio é comum no Chrome, apenas ignoramos e deixamos o onend religar.
      if (event.error === 'no-speech') return;
      console.error("Erro voz:", event.error);
    };

    recognitionRef.current = rec;
    rec.start();
  };

  const stopRecognition = () => {
    shouldBeListeningRef.current = false;
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    setIsListening(false);
  };

  const toggle = () => {
    if (isListening) {
      stopRecognition();
    } else {
      startRecognition();
    }
  };

  return (
    <button
      type="button"
      onClick={toggle}
      className={`flex items-center space-x-2 px-5 py-2.5 rounded-full border transition-all duration-300 ${
        isListening 
        ? 'bg-red-600 text-white border-red-400 shadow-[0_0_20px_rgba(220,38,38,0.4)] animate-pulse' 
        : 'bg-white text-slate-600 border-slate-200 hover:border-blue-400 hover:text-blue-600 shadow-sm'
      }`}
    >
      <Icons.Mic />
      <span className="text-[11px] font-black uppercase tracking-widest">
        {isListening ? "Gravando... (Clique para parar)" : "Ditar com voz"}
      </span>
    </button>
  );
};

// --- Sidebar (Menu Lateral) ---
const Sidebar: React.FC<{ currentTab: AppTab; setTab: (tab: AppTab) => void }> = ({ currentTab, setTab }) => {
  const menuItems = [
    { id: AppTab.TUTORES, icon: <Icons.Tutor />, label: "Tutores" },
    { id: AppTab.PETS, icon: <Icons.Pet />, label: "Pacientes" },
    { id: AppTab.PRONTUARIO, icon: <Icons.Record />, label: "Prontuário" },
    { id: AppTab.BACKUP, icon: <Icons.Backup />, label: "Dados & Backup" },
  ];

  return (
    <div className="w-64 bg-white border-r h-screen flex flex-col fixed left-0 top-0 z-30 shadow-2xl">
      <div className="p-8 border-b bg-slate-50">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center text-white font-black text-2xl shadow-lg shadow-blue-200">RV</div>
          <div>
            <h1 className="text-xl font-black text-slate-800 tracking-tighter leading-none">Ribeira</h1>
            <p className="text-blue-600 font-bold text-[10px] uppercase tracking-[3px] mt-1">Vet Pro AI</p>
          </div>
        </div>
      </div>
      <nav className="flex-1 p-4 space-y-2 mt-6">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setTab(item.id)}
            className={`w-full flex items-center space-x-4 px-6 py-4 rounded-2xl transition-all duration-300 ${
              currentTab === item.id
                ? "bg-blue-600 text-white shadow-xl shadow-blue-100 translate-x-1"
                : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
            }`}
          >
            {item.icon}
            <span className="font-bold text-sm tracking-tight">{item.label}</span>
          </button>
        ))}
      </nav>
      <div className="p-6 border-t bg-slate-50">
        <div className="flex items-center space-x-3 text-emerald-600 bg-emerald-50 p-3 rounded-xl border border-emerald-100">
          <div className="w-2.5 h-2.5 bg-emerald-500 rounded-full animate-ping"></div>
          <span className="text-[10px] font-black uppercase tracking-widest">IA Operacional</span>
        </div>
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

  const addTutor = (t: Omit<Tutor, "id">) => setTutores(prev => [...prev, { ...t, id: crypto.randomUUID() }]);
  const addPet = (p: Pet) => { setPets(prev => [...prev, p]); setActivePetId(p.id); };
  const addRecord = (r: Omit<MedicalRecord, "id">) => setRecords(prev => [...prev, { ...r, id: crypto.randomUUID() }]);
  const restoreBackup = (data: any) => {
    setTutores(data.tutores || []);
    setPets(data.pets || []);
    setRecords(data.records || data.historico || []);
  };

  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <Sidebar currentTab={currentTab} setTab={setCurrentTab} />
      <main className="flex-1 ml-64 p-12 max-w-6xl mx-auto w-full">
        {currentTab === AppTab.TUTORES && <TutorView tutores={tutores} onAdd={addTutor} onGoToPets={() => setCurrentTab(AppTab.PETS)} />}
        {currentTab === AppTab.PETS && <PetView pets={pets} tutores={tutores} onAdd={addPet} onGoToTutores={() => setCurrentTab(AppTab.TUTORES)} onGoToProntuario={(id) => { setActivePetId(id); setCurrentTab(AppTab.PRONTUARIO); }} />}
        {currentTab === AppTab.PRONTUARIO && <ProntuarioView pets={pets} records={records} onAdd={addRecord} onGoToPets={() => setCurrentTab(AppTab.PETS)} selectedId={activePetId} onSelect={setActivePetId} />}
        {currentTab === AppTab.BACKUP && <BackupView data={{ tutores, pets, records }} onRestore={restoreBackup} />}
      </main>
    </div>
  );
}

// --- TutorView ---
const TutorView: React.FC<{ tutores: Tutor[], onAdd: (t: Omit<Tutor, "id">) => void, onGoToPets: () => void }> = ({ tutores, onAdd, onGoToPets }) => {
  const [form, setForm] = useState({ nome: "", cpf: "", tel: "", email: "", endereco: "" });
  const [added, setAdded] = useState(false);

  return (
    <div className="space-y-10 animate-fadeIn">
      <header>
        <h2 className="text-4xl font-black text-slate-800 tracking-tight">Tutores</h2>
        <p className="text-slate-500 text-lg">Cadastro de novos proprietários.</p>
      </header>
      
      {added && (
        <div className="bg-emerald-600 text-white p-6 rounded-[30px] shadow-xl flex justify-between items-center animate-bounce font-bold">
          <span>✅ Tutor cadastrado com sucesso!</span>
          <button onClick={onGoToPets} className="bg-white text-emerald-700 px-6 py-2 rounded-2xl text-xs uppercase font-black hover:bg-slate-100 transition-all">Cadastrar Pet</button>
        </div>
      )}

      <form onSubmit={e => { e.preventDefault(); onAdd({...form, nome: form.nome.toUpperCase()}); setForm({nome:"", cpf:"", tel:"", email:"", endereco:""}); setAdded(true); setTimeout(() => setAdded(false), 5000); }} className="bg-white p-12 rounded-[50px] shadow-2xl border border-slate-100 space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-2">
            <label className="text-[11px] font-black text-slate-400 uppercase tracking-widest ml-4">Nome Completo *</label>
            <input placeholder="JOÃO DA SILVA" required className="w-full p-5 bg-slate-50 rounded-3xl outline-none focus:ring-4 focus:ring-blue-100 transition-all font-bold text-slate-700" value={form.nome} onChange={e => setForm({...form, nome: e.target.value})} />
          </div>
          <div className="space-y-2">
            <label className="text-[11px] font-black text-slate-400 uppercase tracking-widest ml-4">CPF / Identidade *</label>
            <input placeholder="000.000.000-00" required className="w-full p-5 bg-slate-50 rounded-3xl outline-none focus:ring-4 focus:ring-blue-100 transition-all font-bold text-slate-700" value={form.cpf} onChange={e => setForm({...form, cpf: e.target.value})} />
          </div>
          <div className="space-y-2">
            <label className="text-[11px] font-black text-slate-400 uppercase tracking-widest ml-4">WhatsApp</label>
            <input placeholder="(00) 00000-0000" className="w-full p-5 bg-slate-50 rounded-3xl outline-none transition-all font-medium text-slate-700" value={form.tel} onChange={e => setForm({...form, tel: e.target.value})} />
          </div>
          <div className="space-y-2">
            <label className="text-[11px] font-black text-slate-400 uppercase tracking-widest ml-4">E-mail</label>
            <input placeholder="exemplo@gmail.com" type="email" className="w-full p-5 bg-slate-50 rounded-3xl outline-none transition-all font-medium text-slate-700" value={form.email} onChange={e => setForm({...form, email: e.target.value})} />
          </div>
          <div className="md:col-span-2 space-y-2">
            <label className="text-[11px] font-black text-slate-400 uppercase tracking-widest ml-4">Endereço Residencial</label>
            <input placeholder="Rua, Número, Bairro, Cidade" className="w-full p-5 bg-slate-50 rounded-3xl outline-none transition-all font-medium text-slate-700" value={form.endereco} onChange={e => setForm({...form, endereco: e.target.value})} />
          </div>
        </div>
        <button className="w-full bg-blue-600 text-white py-6 rounded-[30px] font-black text-xl hover:bg-blue-700 transition-all shadow-2xl shadow-blue-200 uppercase tracking-widest">Salvar Tutor</button>
      </form>
    </div>
  );
};

// --- PetView ---
const PetView: React.FC<{ pets: Pet[], tutores: Tutor[], onAdd: (p: Pet) => void, onGoToTutores: () => void, onGoToProntuario: (id: string) => void }> = ({ pets, tutores, onAdd, onGoToTutores, onGoToProntuario }) => {
  const [form, setForm] = useState({ nome: "", raca: "", nascimento: "", tutorId: "" });
  
  if (tutores.length === 0) return (
    <div className="flex flex-col items-center justify-center py-32 px-10 bg-white rounded-[60px] shadow-sm border-2 border-dashed border-slate-200">
      <Icons.Warning />
      <h3 className="mt-6 text-2xl font-black text-slate-800">Nenhum tutor na base</h3>
      <p className="text-slate-400 text-center max-w-sm mt-2 font-medium">Você precisa cadastrar um tutor antes de registrar o paciente.</p>
      <button onClick={onGoToTutores} className="mt-10 bg-blue-600 text-white px-12 py-5 rounded-3xl font-black shadow-xl shadow-blue-100 hover:scale-105 transition-transform">Ir para Tutores</button>
    </div>
  );

  return (
    <div className="space-y-10 animate-fadeIn">
      <header><h2 className="text-4xl font-black text-slate-800 tracking-tight">Pacientes</h2></header>
      
      <form onSubmit={(e) => { e.preventDefault(); onAdd({...form, id: crypto.randomUUID(), nome: form.nome.toUpperCase(), raca: form.raca.toUpperCase()}); setForm({nome:"", raca:"", nascimento:"", tutorId:form.tutorId}); }} className="bg-white p-12 rounded-[50px] shadow-2xl border border-slate-100 space-y-8">
        <div className="space-y-2">
          <label className="text-[11px] font-black text-slate-400 uppercase tracking-widest ml-6">Proprietário / Responsável *</label>
          <select required className="w-full p-6 bg-slate-50 rounded-[30px] outline-none focus:ring-4 focus:ring-blue-100 transition-all font-black text-slate-700 appearance-none cursor-pointer" value={form.tutorId} onChange={e => setForm({...form, tutorId: e.target.value})}>
            <option value="">Selecione o Tutor</option>
            {tutores.map(t => <option key={t.id} value={t.id}>{t.nome}</option>)}
          </select>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-2">
            <label className="text-[11px] font-black text-slate-400 uppercase tracking-widest ml-6">Nome do Pet *</label>
            <input placeholder="EX: THOR" required className="w-full p-6 bg-slate-50 rounded-[30px] font-bold text-slate-700 outline-none focus:ring-4 focus:ring-blue-50" value={form.nome} onChange={e => setForm({...form, nome: e.target.value})} />
          </div>
          <div className="space-y-2">
            <label className="text-[11px] font-black text-slate-400 uppercase tracking-widest ml-6">Raça / Espécie</label>
            <input placeholder="EX: PUG" className="w-full p-6 bg-slate-50 rounded-[30px] font-bold text-slate-700 outline-none" value={form.raca} onChange={e => setForm({...form, raca: e.target.value})} />
          </div>
        </div>
        <button className="w-full bg-slate-900 text-white py-6 rounded-[35px] font-black text-xl hover:bg-black shadow-2xl transition-all uppercase tracking-widest">Cadastrar Paciente</button>
      </form>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
        {pets.map(p => (
          <div key={p.id} className="bg-white p-10 rounded-[45px] shadow-lg border border-slate-50 hover:shadow-2xl transition-all group relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-50 rounded-bl-full -mr-12 -mt-12 group-hover:bg-blue-100 transition-colors"></div>
            <h4 className="font-black text-3xl text-slate-800 mb-1">{p.nome}</h4>
            <p className="text-xs font-black text-blue-600 uppercase tracking-widest mb-6">{p.raca || "Sem raça definida"}</p>
            <div className="flex items-center text-xs text-slate-400 font-bold mb-8">
              <Icons.Tutor /> <span className="ml-2 truncate max-w-[150px]">{tutores.find(t => t.id === p.tutorId)?.nome}</span>
            </div>
            <button onClick={() => onGoToProntuario(p.id)} className="w-full py-4 bg-slate-50 text-slate-800 rounded-2xl font-black text-xs hover:bg-blue-600 hover:text-white transition-all flex items-center justify-center space-x-2">
              <Icons.Record /> <span>Abrir Prontuário</span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

// --- ProntuarioView ---
const ProntuarioView: React.FC<{ pets: Pet[], records: MedicalRecord[], onAdd: (r: Omit<MedicalRecord, "id">) => void, onGoToPets: () => void, selectedId: string, onSelect: (id: string) => void }> = ({ pets, records, onAdd, onGoToPets, selectedId, onSelect }) => {
  const [sin, setSin] = useState("");
  const [obs, setObs] = useState("");
  const [loading, setLoading] = useState(false);
  const [ai, setAi] = useState("");

  const handleVoice = (field: 'sin' | 'obs', text: string) => {
    // Adiciona o texto novo ao final do que já existe, garantindo fluxo contínuo.
    if (field === 'sin') setSin(prev => prev ? `${prev} ${text}` : text);
    else setObs(prev => prev ? `${prev} ${text}` : text);
  };

  const selectedPet = pets.find(p => p.id === selectedId);

  return (
    <div className="space-y-12 pb-32 animate-fadeIn">
      <header>
        <h2 className="text-4xl font-black text-slate-800 tracking-tight">Atendimento Clínico</h2>
        <p className="text-slate-500 text-lg">Prontuário veterinário inteligente.</p>
      </header>
      
      <div className="bg-white p-12 rounded-[60px] shadow-2xl border border-white space-y-10">
        <div className="space-y-4">
          <label className="text-xs font-black text-slate-400 uppercase tracking-[4px] ml-8">Paciente em Consulta *</label>
          <select className="w-full p-8 bg-slate-50 rounded-[40px] font-black text-2xl border-none focus:ring-8 focus:ring-blue-50 text-slate-800 appearance-none text-center cursor-pointer shadow-inner" value={selectedId} onChange={e => { onSelect(e.target.value); setAi(""); }}>
            <option value="">Selecione o Pet no Consultório</option>
            {pets.map(p => <option key={p.id} value={p.id}>{p.nome} ({p.raca})</option>)}
          </select>
        </div>

        {selectedId && (
          <div className="space-y-12 mt-10 animate-fadeIn">
            <div className="space-y-4">
              <div className="flex justify-between items-center px-6">
                <label className="text-xs font-black text-slate-400 uppercase tracking-widest">Anamnese / Sintomas</label>
                <VoiceButton onResult={(t) => handleVoice('sin', t)} />
              </div>
              <textarea className="w-full p-10 bg-slate-50 rounded-[50px] min-h-[220px] outline-none focus:bg-white focus:ring-4 focus:ring-blue-50 text-xl font-medium leading-relaxed text-slate-700 shadow-inner" placeholder="Clique no microfone para ditar o que o tutor relatou ou escreva aqui..." value={sin} onChange={e => setSin(e.target.value)} />
              <button onClick={async () => { if(!sin || !selectedPet) return; setLoading(true); const res = await getAiDiagnosisSuggestion(sin, {nome:selectedPet.nome, raca:selectedPet.raca}); setAi(res || ""); setLoading(false); }} disabled={loading || !sin} className="flex items-center space-x-3 bg-blue-50 text-blue-700 px-10 py-5 rounded-[25px] font-black hover:bg-blue-100 transition-all shadow-sm">
                <Icons.Sparkles /> <span>{loading ? "IA ESTÁ ANALISANDO..." : "Pedir análise da Inteligência Artificial"}</span>
              </button>
            </div>

            {ai && (
              <div className="bg-gradient-to-br from-blue-700 to-indigo-900 p-12 rounded-[60px] text-white shadow-2xl animate-slideUp leading-relaxed relative overflow-hidden">
                <div className="absolute top-0 right-0 p-12 opacity-10"><Icons.AI /></div>
                <div className="flex items-center space-x-3 mb-8 font-black border-b border-white/20 pb-6 text-sm tracking-[3px] uppercase">
                  <Icons.Sparkles /> <span>Sugestão Veterinária Pro AI</span>
                </div>
                <div className="whitespace-pre-wrap text-xl opacity-90">{ai}</div>
              </div>
            )}

            <div className="space-y-4">
              <div className="flex justify-between items-center px-6">
                <label className="text-xs font-black text-slate-400 uppercase tracking-widest">Conduta / Tratamento</label>
                <VoiceButton onResult={(t) => handleVoice('obs', t)} />
              </div>
              <textarea className="w-full p-10 bg-slate-50 rounded-[50px] min-h-[220px] outline-none focus:bg-white focus:ring-4 focus:ring-blue-50 text-xl font-medium leading-relaxed text-slate-700 shadow-inner" placeholder="Quais foram as recomendações, medicamentos e doses?" value={obs} onChange={e => setObs(e.target.value)} />
            </div>

            <button onClick={() => { onAdd({ petId: selectedId, data: new Date().toLocaleDateString("pt-BR"), observacoes: obs, sintomas: sin, diagnosticoAi: ai }); setSin(""); setObs(""); setAi(""); alert("✅ Consulta registrada com sucesso!"); }} className="w-full bg-slate-900 text-white py-8 rounded-[40px] font-black text-2xl uppercase tracking-[4px] shadow-2xl hover:scale-[1.01] transition-transform">Finalizar Consulta</button>
          </div>
        )}
      </div>

      {/* Histórico do Paciente */}
      <div className="space-y-10 mt-20">
        <h3 className="font-black text-4xl text-slate-800 flex items-center space-x-4 ml-4">
          <div className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center shadow-md"><Icons.Record /></div>
          <span>Histórico Médico</span>
        </h3>
        <div className="space-y-8">
          {records.filter(r => r.petId === selectedId).reverse().map(r => (
            <div key={r.id} className="bg-white p-12 rounded-[55px] border border-slate-100 shadow-xl transition-all hover:shadow-2xl flex flex-col md:flex-row gap-12">
              <div className="flex-shrink-0">
                <span className="text-xs font-black text-blue-600 bg-blue-50 px-8 py-3 rounded-full uppercase tracking-widest border border-blue-100">{r.data}</span>
              </div>
              <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-12">
                <div className="space-y-4">
                  <p className="font-black text-slate-300 uppercase text-[10px] tracking-[5px] border-b pb-3">Anamnese</p>
                  <p className="text-slate-700 text-xl font-medium leading-relaxed">{r.sintomas || "Sem registro."}</p>
                </div>
                <div className="space-y-4">
                  <p className="font-black text-slate-300 uppercase text-[10px] tracking-[5px] border-b pb-3">Conduta Clínica</p>
                  <p className="text-slate-700 text-xl font-bold leading-relaxed">{r.observacoes || "Sem registro."}</p>
                </div>
              </div>
            </div>
          ))}
          {records.filter(r => r.petId === selectedId).length === 0 && selectedId && (
            <div className="p-20 text-center text-slate-300 font-black text-2xl bg-white rounded-[60px] border-4 border-dashed border-slate-50 uppercase tracking-widest">Nenhuma consulta anterior</div>
          )}
        </div>
      </div>
    </div>
  );
};

// --- BackupView ---
const BackupView: React.FC<{ data: any, onRestore: (d: any) => void }> = ({ data, onRestore }) => (
  <div className="space-y-12 animate-fadeIn">
    <header>
      <h2 className="text-4xl font-black text-slate-800 tracking-tight">Segurança de Dados</h2>
      <p className="text-slate-500 text-lg">Sempre faça backup após o dia de atendimentos.</p>
    </header>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
      <button onClick={() => { const b = new Blob([JSON.stringify(data, null, 2)], {type:"application/json"}); const u = URL.createObjectURL(b); const a = document.createElement("a"); a.href = u; a.download = `RIBEIRA_VET_BACKUP_${new Date().toLocaleDateString("pt-BR").replace(/\//g, '-')}.json`; a.click(); }} className="bg-white p-24 rounded-[70px] border-2 border-slate-50 shadow-xl flex flex-col items-center space-y-10 group hover:shadow-2xl transition-all active:scale-95">
        <div className="w-28 h-28 bg-emerald-50 text-emerald-600 rounded-[40px] flex items-center justify-center text-5xl group-hover:scale-110 transition-transform duration-500 shadow-inner"><Icons.Backup /></div>
        <div className="text-center">
          <h4 className="font-black text-3xl text-slate-800 uppercase tracking-tighter">Baixar Base</h4>
          <p className="text-slate-400 mt-3 font-bold">Salva tudo em um arquivo JSON seguro.</p>
        </div>
      </button>
      <div className="relative bg-white p-24 rounded-[70px] border-2 border-slate-50 shadow-xl flex flex-col items-center space-y-10 group hover:shadow-2xl transition-all cursor-pointer active:scale-95">
        <input type="file" className="absolute inset-0 opacity-0 cursor-pointer z-10" onChange={(e) => { const f = e.target.files?.[0]; if(!f) return; const r = new FileReader(); r.onload=(ev) => { try { onRestore(JSON.parse(ev.target?.result as string)); alert("✅ Base de dados restaurada com sucesso!"); } catch { alert("❌ Arquivo inválido ou corrompido."); } }; r.readAsText(f); }} />
        <div className="w-28 h-28 bg-amber-50 text-amber-600 rounded-[40px] flex items-center justify-center text-5xl group-hover:scale-110 transition-transform duration-500 shadow-inner"><Icons.Warning /></div>
        <div className="text-center">
          <h4 className="font-black text-3xl text-slate-800 uppercase tracking-tighter">Restaurar</h4>
          <p className="text-slate-400 mt-3 font-bold">Recupera dados de um backup anterior.</p>
        </div>
      </div>
    </div>
  </div>
);
