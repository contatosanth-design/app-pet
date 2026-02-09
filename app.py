
import React, { useState, useEffect, useRef } from 'react';
import { Tutor, Pet, MedicalRecord, AppTab } from './types';
import { getAiDiagnosisSuggestion } from './services/geminiService';

// --- Ícones ---
const Icons = {
  Tutor: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>,
  Pet: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>,
  Record: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>,
  Backup: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" /></svg>,
  AI: () => <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 10-2 0v1a1 1 0 102 0v-1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 10-2 0v1a1 1 0 102 0v-1zM8 16v-1a1 1 0 10-2 0v1a1 1 0 102 0zM12 16v-1a1 1 0 10-2 0v1a1 1 0 102 0zM16 16v-1a1 1 0 10-2 0v1a1 1 0 102 0z" /></svg>,
  Check: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" /></svg>,
  Mic: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 10v2a7 7 0 01-14 0v-2m7 9v3m-3 0h6" /></svg>,
  Sparkles: () => <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" /></svg>,
  Warning: () => <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
};

// --- Componente de Botão de Voz com Religamento Automático ---
const VoiceButton: React.FC<{ onResult: (text: string) => void }> = ({ onResult }) => {
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<any>(null);
  const manualStopRef = useRef(false);

  const startListening = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    const recognition = new SpeechRecognition();
    recognition.lang = 'pt-BR';
    recognition.continuous = true;
    recognition.interimResults = false;

    recognition.onstart = () => {
      setIsListening(true);
      manualStopRef.current = false;
    };

    recognition.onend = () => {
      // Se NÃO foi um stop manual, religa o microfone automaticamente
      if (!manualStopRef.current) {
        try {
          recognition.start();
        } catch (e) {
          console.error("Erro ao religar:", e);
        }
      } else {
        setIsListening(false);
      }
    };

    recognition.onresult = (event: any) => {
      const lastIndex = event.results.length - 1;
      const transcript = event.results[lastIndex][0].transcript;
      if (event.results[lastIndex].isFinal) {
        onResult(transcript);
      }
    };

    recognition.onerror = (event: any) => {
      if (event.error === 'no-speech') return; // Ignora erro de silêncio para manter ativo
      console.error("Erro voz:", event.error);
    };

    recognitionRef.current = recognition;
    recognition.start();
  };

  const toggle = () => {
    if (isListening) {
      manualStopRef.current = true;
      if (recognitionRef.current) recognitionRef.current.stop();
      setIsListening(false);
    } else {
      startListening();
    }
  };

  return (
    <button
      type="button"
      onClick={toggle}
      className={`flex items-center space-x-2 px-4 py-2 rounded-full border transition-all ${
        isListening 
        ? 'bg-red-600 text-white border-red-400 shadow-[0_0_15px_rgba(220,38,38,0.5)] animate-pulse' 
        : 'bg-slate-50 text-slate-500 border-slate-200 hover:bg-blue-50 hover:text-blue-600'
      }`}
    >
      <Icons.Mic />
      <span className="text-[10px] font-bold uppercase tracking-widest">
        {isListening ? "Gravando (Fale agora)" : "Ditar texto"}
      </span>
    </button>
  );
};

// --- Sidebar ---
const Sidebar: React.FC<{ currentTab: AppTab; setTab: (tab: AppTab) => void }> = ({ currentTab, setTab }) => {
  const menuItems = [
    { id: AppTab.TUTORES, icon: <Icons.Tutor />, label: "Tutores" },
    { id: AppTab.PETS, icon: <Icons.Pet />, label: "Pets" },
    { id: AppTab.PRONTUARIO, icon: <Icons.Record />, label: "Prontuário" },
    { id: AppTab.BACKUP, icon: <Icons.Backup />, label: "Backup" },
  ];

  return (
    <div className="w-64 bg-white border-r h-screen flex flex-col fixed left-0 top-0 z-10 shadow-sm">
      <div className="p-6 border-b flex items-center space-x-3">
        <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white font-black text-xl shadow-lg shadow-blue-200">RV</div>
        <h1 className="text-xl font-bold text-slate-800 leading-tight">Ribeira<br/><span className="text-blue-600">Vet Pro</span></h1>
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setTab(item.id)}
            className={`w-full flex items-center space-x-3 px-4 py-3.5 rounded-2xl transition-all duration-200 ${
              currentTab === item.id
                ? "bg-blue-600 text-white shadow-lg shadow-blue-200 translate-x-1"
                : "text-slate-500 hover:bg-slate-50 hover:text-slate-800"
            }`}
          >
            {item.icon}
            <span className="font-semibold">{item.label}</span>
          </button>
        ))}
      </nav>
      <div className="p-6 border-t">
        <div className="bg-slate-50 p-3 rounded-xl">
          <p className="text-[10px] font-black text-slate-400 uppercase tracking-[2px] mb-1">Status do Sistema</p>
          <div className="flex items-center space-x-2 text-green-600">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-ping"></div>
            <span className="text-xs font-bold">Online & AI Ativa</span>
          </div>
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
    <div className="flex min-h-screen bg-[#f8fafc]">
      <Sidebar currentTab={currentTab} setTab={setCurrentTab} />
      <main className="flex-1 ml-64 p-10 max-w-6xl mx-auto w-full">
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

  return (
    <div className="space-y-8 animate-fadeIn">
      <header>
        <h2 className="text-4xl font-black text-slate-800 tracking-tight">Tutores</h2>
        <p className="text-slate-500 text-lg">Gerenciamento de proprietários e clientes.</p>
      </header>
      
      {added && (
        <div className="bg-green-50 p-5 rounded-2xl border border-green-200 flex justify-between items-center text-green-700 font-bold shadow-sm animate-bounce">
          <div className="flex items-center space-x-2"><Icons.Check /> <span>Tutor cadastrado com sucesso!</span></div>
          <button onClick={onGoToPets} className="bg-green-600 text-white px-6 py-2 rounded-xl text-sm hover:bg-green-700 transition-all">CADASTRAR PET</button>
        </div>
      )}

      <form onSubmit={e => { e.preventDefault(); onAdd({...form, nome: form.nome.toUpperCase()}); setForm({nome:"", cpf:"", tel:"", email:"", endereco:""}); setAdded(true); setTimeout(() => setAdded(false), 5000); }} className="bg-white p-10 rounded-[40px] shadow-xl border border-slate-100 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-[11px] font-black text-slate-400 uppercase ml-4">Nome Completo *</label>
            <input placeholder="EX: JOÃO SILVA" required className="w-full p-4 bg-slate-50 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 transition-all text-slate-700 font-medium" value={form.nome} onChange={e => setForm({...form, nome: e.target.value})} />
          </div>
          <div className="space-y-2">
            <label className="text-[11px] font-black text-slate-400 uppercase ml-4">CPF / Documento *</label>
            <input placeholder="000.000.000-00" required className="w-full p-4 bg-slate-50 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 transition-all text-slate-700 font-medium" value={form.cpf} onChange={e => setForm({...form, cpf: e.target.value})} />
          </div>
          <div className="space-y-2">
            <label className="text-[11px] font-black text-slate-400 uppercase ml-4">WhatsApp / Telefone</label>
            <input placeholder="(00) 00000-0000" className="w-full p-4 bg-slate-50 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 transition-all text-slate-700 font-medium" value={form.tel} onChange={e => setForm({...form, tel: e.target.value})} />
          </div>
          <div className="space-y-2">
            <label className="text-[11px] font-black text-slate-400 uppercase ml-4">E-mail</label>
            <input placeholder="cliente@email.com" type="email" className="w-full p-4 bg-slate-50 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 transition-all text-slate-700 font-medium" value={form.email} onChange={e => setForm({...form, email: e.target.value})} />
          </div>
          <div className="md:col-span-2 space-y-2">
            <label className="text-[11px] font-black text-slate-400 uppercase ml-4">Endereço Completo</label>
            <input placeholder="Rua, Número, Bairro, Cidade" className="w-full p-4 bg-slate-50 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 transition-all text-slate-700 font-medium" value={form.endereco} onChange={e => setForm({...form, endereco: e.target.value})} />
          </div>
        </div>
        <button className="w-full bg-blue-600 text-white py-5 rounded-2xl font-black text-lg hover:bg-blue-700 transition-all shadow-xl shadow-blue-100 flex items-center justify-center space-x-2">
          <Icons.Tutor /> <span>SALVAR TUTOR</span>
        </button>
      </form>
    </div>
  );
};

const PetView: React.FC<{ pets: Pet[], tutores: Tutor[], onAdd: (p: Pet) => void, onGoToTutores: () => void, onGoToProntuario: (id: string) => void }> = ({ pets, tutores, onAdd, onGoToTutores, onGoToProntuario }) => {
  const [form, setForm] = useState({ nome: "", raca: "", nascimento: "", tutorId: "" });
  
  if (tutores.length === 0) return (
    <div className="flex flex-col items-center justify-center py-24 px-10 bg-white rounded-[50px] shadow-sm border border-dashed border-slate-300">
      <Icons.Warning />
      <h3 className="mt-4 text-2xl font-bold text-slate-800 text-center">Nenhum tutor cadastrado</h3>
      <p className="text-slate-400 text-center max-w-xs mt-2">Para cadastrar um paciente, primeiro você precisa adicionar um tutor responsável.</p>
      <button onClick={onGoToTutores} className="mt-8 bg-blue-600 text-white px-10 py-4 rounded-2xl font-black shadow-lg">IR PARA TUTORES</button>
    </div>
  );

  return (
    <div className="space-y-8 animate-fadeIn">
      <header><h2 className="text-4xl font-black text-slate-800 tracking-tight">Pacientes</h2></header>
      
      <form onSubmit={(e) => { e.preventDefault(); onAdd({...form, id: crypto.randomUUID(), nome: form.nome.toUpperCase(), raca: form.raca.toUpperCase()}); setForm({nome:"", raca:"", nascimento:"", tutorId:form.tutorId}); }} className="bg-white p-10 rounded-[40px] border border-slate-100 shadow-xl space-y-6">
        <div className="space-y-2">
          <label className="text-[11px] font-black text-slate-400 uppercase ml-4">Proprietário Responsável *</label>
          <select required className="w-full p-4 bg-slate-50 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 transition-all font-bold text-slate-700 appearance-none" value={form.tutorId} onChange={e => setForm({...form, tutorId: e.target.value})}>
            <option value="">SELECIONE O TUTOR</option>
            {tutores.map(t => <option key={t.id} value={t.id}>{t.nome}</option>)}
          </select>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-[11px] font-black text-slate-400 uppercase ml-4">Nome do Pet *</label>
            <input placeholder="EX: THOR" required className="w-full p-4 bg-slate-50 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 transition-all text-slate-700 font-medium" value={form.nome} onChange={e => setForm({...form, nome: e.target.value})} />
          </div>
          <div className="space-y-2">
            <label className="text-[11px] font-black text-slate-400 uppercase ml-4">Raça / Espécie</label>
            <input placeholder="EX: PUG" className="w-full p-4 bg-slate-50 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 transition-all text-slate-700 font-medium" value={form.raca} onChange={e => setForm({...form, raca: e.target.value})} />
          </div>
        </div>
        <button className="w-full bg-blue-600 text-white py-5 rounded-2xl font-black text-lg hover:bg-blue-700 shadow-xl">ADICIONAR PACIENTE</button>
      </form>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-10">
        {pets.map(p => (
          <div key={p.id} className="bg-white p-8 rounded-[35px] border border-slate-100 shadow-md hover:shadow-2xl transition-all group relative overflow-hidden">
            <div className="absolute top-0 right-0 w-24 h-24 bg-blue-50 rounded-bl-[100px] -mr-8 -mt-8 group-hover:bg-blue-100 transition-colors"></div>
            <h4 className="font-black text-2xl text-slate-800 mb-1">{p.nome}</h4>
            <p className="text-xs font-black text-blue-600 uppercase tracking-widest mb-4">{p.raca || "Raça indefinida"}</p>
            <div className="flex items-center text-xs text-slate-400 font-bold mb-6">
              <Icons.Tutor /> <span className="ml-2">{tutores.find(t => t.id === p.tutorId)?.nome}</span>
            </div>
            <button onClick={() => onGoToProntuario(p.id)} className="w-full py-3 bg-slate-800 text-white rounded-xl font-bold text-xs hover:bg-blue-600 transition-colors flex items-center justify-center space-x-2">
              <Icons.Record /> <span>ABRIR PRONTUÁRIO</span>
            </button>
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

  const handleVoice = (field: 'sin' | 'obs', text: string) => {
    if (field === 'sin') setSin(prev => prev ? `${prev} ${text}` : text);
    else setObs(prev => prev ? `${prev} ${text}` : text);
  };

  const selectedPet = pets.find(p => p.id === selectedId);

  return (
    <div className="space-y-8 pb-32 animate-fadeIn">
      <header className="flex justify-between items-end">
        <div>
          <h2 className="text-4xl font-black text-slate-800 tracking-tight">Atendimento</h2>
          <p className="text-slate-500 text-lg">Prontuário e diagnóstico assistido.</p>
        </div>
      </header>
      
      <div className="bg-white p-10 rounded-[50px] border border-slate-100 shadow-2xl space-y-8">
        <div className="space-y-2">
          <label className="text-[11px] font-black text-slate-400 uppercase ml-6 tracking-widest">Paciente em Atendimento *</label>
          <select className="w-full p-6 bg-slate-50 rounded-[30px] font-black text-xl border-none focus:ring-4 focus:ring-blue-100 transition-all text-slate-800 cursor-pointer shadow-inner" value={selectedId} onChange={e => { onSelect(e.target.value); setAi(""); }}>
            <option value="">SELECIONE O PET NO CONSULTÓRIO</option>
            {pets.map(p => <option key={p.id} value={p.id}>{p.nome} - {p.raca}</option>)}
          </select>
        </div>

        {selectedId && (
          <div className="space-y-10 mt-6 animate-fadeIn">
            {/* Seção Anamnese */}
            <div className="space-y-4">
              <div className="flex justify-between items-center px-4">
                <label className="text-xs font-black text-slate-400 uppercase tracking-widest">Anamnese / Sintomas Relatados</label>
                <VoiceButton onResult={(t) => handleVoice('sin', t)} />
              </div>
              <textarea className="w-full p-8 bg-slate-50 rounded-[40px] min-h-[160px] outline-none focus:bg-white focus:ring-4 focus:ring-blue-50 transition-all text-slate-700 text-lg font-medium leading-relaxed shadow-inner" placeholder="Clique no microfone para ditar ou escreva o que o pet apresenta..." value={sin} onChange={e => setSin(e.target.value)} />
              <button onClick={async () => { if(!sin || !selectedPet) return; setLoading(true); const res = await getAiDiagnosisSuggestion(sin, {nome:selectedPet.nome, raca:selectedPet.raca}); setAi(res || ""); setLoading(false); }} disabled={loading || !sin} className="flex items-center space-x-3 bg-blue-50 text-blue-700 px-8 py-4 rounded-[20px] font-black hover:bg-blue-100 transition-all shadow-sm">
                <Icons.Sparkles /> <span>{loading ? "IA ANALISANDO..." : "SOLICITAR OPINIÃO DA IA"}</span>
              </button>
            </div>

            {/* Sugestão da IA */}
            {ai && (
              <div className="bg-gradient-to-br from-blue-700 to-blue-900 p-10 rounded-[50px] text-white shadow-2xl animate-slideUp leading-relaxed relative overflow-hidden">
                <div className="absolute top-0 right-0 p-8 opacity-10"><Icons.AI /></div>
                <div className="flex items-center space-x-2 mb-6 font-black border-b border-blue-400/30 pb-4 text-sm tracking-widest uppercase"><Icons.Sparkles /><span>Análise Veterinaria Pro AI</span></div>
                <div className="whitespace-pre-wrap text-lg opacity-90">{ai}</div>
              </div>
            )}

            {/* Conduta */}
            <div className="space-y-4">
              <div className="flex justify-between items-center px-4">
                <label className="text-xs font-black text-slate-400 uppercase tracking-widest">Conduta / Tratamento Prescrito</label>
                <VoiceButton onResult={(t) => handleVoice('obs', t)} />
              </div>
              <textarea className="w-full p-8 bg-slate-50 rounded-[40px] min-h-[160px] outline-none focus:bg-white focus:ring-4 focus:ring-blue-50 transition-all text-slate-700 text-lg font-medium leading-relaxed shadow-inner" placeholder="Qual o plano de tratamento e medicamentos?" value={obs} onChange={e => setObs(e.target.value)} />
            </div>

            <button onClick={() => { onAdd({ petId: selectedId, data: new Date().toLocaleDateString("pt-BR"), observacoes: obs, sintomas: sin, diagnosticoAi: ai }); setSin(""); setObs(""); setAi(""); alert("Atendimento registrado com sucesso!"); }} className="w-full bg-slate-900 text-white py-6 rounded-[30px] font-black text-xl uppercase tracking-[2px] shadow-2xl hover:bg-black transition-all hover:scale-[1.01]">FINALIZAR CONSULTA</button>
          </div>
        )}
      </div>

      {/* Histórico Recente */}
      <div className="space-y-8 mt-16">
        <h3 className="font-black text-3xl text-slate-800 flex items-center space-x-3"><Icons.Record /><span>Histórico do Paciente</span></h3>
        <div className="space-y-6">
          {records.filter(r => r.petId === selectedId).reverse().map(r => (
            <div key={r.id} className="bg-white p-10 rounded-[45px] border border-slate-100 shadow-xl transition-all hover:shadow-2xl flex flex-col md:flex-row md:items-start gap-8">
              <div className="flex-shrink-0"><span className="text-xs font-black text-blue-600 bg-blue-50 px-6 py-2 rounded-full uppercase tracking-widest">{r.data}</span></div>
              <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-10">
                <div className="space-y-3">
                  <p className="font-black text-slate-300 uppercase text-[10px] tracking-[3px] border-b pb-2">Anamnese</p>
                  <p className="text-slate-700 text-lg leading-relaxed">{r.sintomas || "Sem relato registrado."}</p>
                </div>
                <div className="space-y-3">
                  <p className="font-black text-slate-300 uppercase text-[10px] tracking-[3px] border-b pb-2">Conduta Clínica</p>
                  <p className="text-slate-700 text-lg leading-relaxed font-bold">{r.observacoes || "Sem conduta registrada."}</p>
                </div>
              </div>
            </div>
          ))}
          {records.filter(r => r.petId === selectedId).length === 0 && selectedId && (
            <div className="p-10 text-center text-slate-400 font-bold bg-white rounded-3xl border border-dashed">Paciente sem atendimentos anteriores.</div>
          )}
        </div>
      </div>
    </div>
  );
};

const BackupView: React.FC<{ data: any, onRestore: (d: any) => void }> = ({ data, onRestore }) => (
  <div className="space-y-10 animate-fadeIn">
    <header>
      <h2 className="text-4xl font-black text-slate-800 tracking-tight">Segurança</h2>
      <p className="text-slate-500 text-lg">Sempre baixe o backup após os atendimentos.</p>
    </header>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
      <button onClick={() => { const blob = new Blob([JSON.stringify(data, null, 2)], {type:"application/json"}); const url = URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = `BACKUP_RIBEIRA_VET_${new Date().toISOString().split('T')[0]}.json`; a.click(); }} className="bg-white p-16 rounded-[60px] border border-slate-100 shadow-xl flex flex-col items-center space-y-8 hover:shadow-2xl transition-all group active:scale-95">
        <div className="w-24 h-24 bg-green-50 text-green-600 rounded-[35px] flex items-center justify-center text-4xl group-hover:scale-110 transition-transform duration-300"><Icons.Backup /></div>
        <div className="text-center">
          <h4 className="font-black text-2xl text-slate-800">Exportar Base</h4>
          <p className="text-slate-400 mt-2 font-medium">Baixa o arquivo de segurança para o seu computador.</p>
        </div>
      </button>
      <div className="relative bg-white p-16 rounded-[60px] border border-slate-100 shadow-xl flex flex-col items-center space-y-8 hover:shadow-2xl transition-all group cursor-pointer active:scale-95">
        <input type="file" className="absolute inset-0 opacity-0 cursor-pointer z-10" onChange={(e) => { const f = e.target.files?.[0]; if(!f) return; const r = new FileReader(); r.onload=(ev) => { try { onRestore(JSON.parse(ev.target?.result as string)); alert("✅ Banco de dados restaurado com sucesso!"); } catch { alert("❌ Arquivo inválido ou corrompido."); } }; r.readAsText(f); }} />
        <div className="w-24 h-24 bg-amber-50 text-amber-600 rounded-[35px] flex items-center justify-center text-4xl group-hover:scale-110 transition-transform duration-300"><Icons.Warning /></div>
        <div className="text-center">
          <h4 className="font-black text-2xl text-slate-800">Restaurar Backup</h4>
          <p className="text-slate-400 mt-2 font-medium">Recupera dados de um arquivo baixado anteriormente.</p>
        </div>
      </div>
    </div>
  </div>
);
