
import React, { useState, useEffect, useRef } from 'react';
import { Tutor, Pet, MedicalRecord, AppTab } from './types';
import { getAiDiagnosisSuggestion } from './services/geminiService';

// --- Componentes de Ícones Profissionais ---
const Icons = {
  Tutor: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>,
  Pet: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>,
  Record: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>,
  Backup: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" /></svg>,
  Mic: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 10v2a7 7 0 01-14 0v-2m7 9v3m-3 0h6" /></svg>,
  Sparkles: () => <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" /></svg>,
  Check: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" /></svg>,
  AI: () => <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 10-2 0v1a1 1 0 102 0v-1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 10-2 0v1a1 1 0 102 0v-1zM8 16v-1a1 1 0 10-2 0v1a1 1 0 102 0zM12 16v-1a1 1 0 10-2 0v1a1 1 0 102 0zM16 16v-1a1 1 0 10-2 0v1a1 1 0 102 0z" /></svg>
};

// --- Botão de Voz Ininterrupto ---
const VoiceButton: React.FC<{ onResult: (text: string) => void }> = ({ onResult }) => {
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<any>(null);
  const activeRef = useRef(false);

  const start = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    const rec = new SpeechRecognition();
    rec.lang = 'pt-BR';
    rec.continuous = true;
    rec.interimResults = false;

    rec.onstart = () => {
      setIsListening(true);
      activeRef.current = true;
    };

    rec.onend = () => {
      // Se o sistema desligar por silêncio, mas o médico ainda quer ditar, ele religa imediatamente.
      if (activeRef.current) {
        setTimeout(() => {
          try { rec.start(); } catch (e) { console.log("Reativando..."); }
        }, 100);
      } else {
        setIsListening(false);
      }
    };

    rec.onresult = (event: any) => {
      const last = event.results.length - 1;
      const text = event.results[last][0].transcript;
      if (event.results[last].isFinal) onResult(text);
    };

    rec.onerror = (e: any) => {
      if (e.error === 'no-speech') return; 
      console.error("Status Voz:", e.error);
    };

    recognitionRef.current = rec;
    rec.start();
  };

  const toggle = () => {
    if (isListening) {
      activeRef.current = false;
      if (recognitionRef.current) recognitionRef.current.stop();
      setIsListening(false);
    } else {
      start();
    }
  };

  return (
    <button
      type="button"
      onClick={toggle}
      className={`flex items-center space-x-3 px-6 py-3 rounded-2xl border transition-all duration-300 ${
        isListening 
        ? 'bg-red-600 text-white border-red-400 shadow-xl scale-105 animate-pulse' 
        : 'bg-white text-slate-600 border-slate-200 hover:border-blue-400 hover:text-blue-600 shadow-sm'
      }`}
    >
      <Icons.Mic />
      <span className="text-xs font-black uppercase tracking-widest">
        {isListening ? "Gravando dita..." : "Ditar por voz"}
      </span>
    </button>
  );
};

// --- Sidebar ---
const Sidebar: React.FC<{ currentTab: AppTab; setTab: (tab: AppTab) => void }> = ({ currentTab, setTab }) => {
  const menu = [
    { id: AppTab.TUTORES, icon: <Icons.Tutor />, label: "Tutores" },
    { id: AppTab.PETS, icon: <Icons.Pet />, label: "Pacientes" },
    { id: AppTab.PRONTUARIO, icon: <Icons.Record />, label: "Prontuário" },
    { id: AppTab.BACKUP, icon: <Icons.Backup />, label: "Dados" },
  ];

  return (
    <div className="w-64 bg-white border-r h-screen flex flex-col fixed left-0 top-0 z-20 shadow-xl">
      <div className="p-8 border-b">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center text-white font-black text-2xl shadow-lg">RV</div>
          <div>
            <h1 className="text-lg font-black text-slate-800 leading-none">Ribeira</h1>
            <span className="text-blue-600 font-bold text-[10px] uppercase tracking-widest">Vet Pro AI</span>
          </div>
        </div>
      </div>
      <nav className="flex-1 p-4 mt-6 space-y-2">
        {menu.map((item) => (
          <button
            key={item.id}
            onClick={() => setTab(item.id)}
            className={`w-full flex items-center space-x-4 px-6 py-4 rounded-2xl transition-all duration-300 ${
              currentTab === item.id
                ? "bg-blue-600 text-white shadow-xl translate-x-1"
                : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
            }`}
          >
            {item.icon}
            <span className="font-bold text-sm tracking-tight">{item.label}</span>
          </button>
        ))}
      </nav>
      <div className="p-6 border-t bg-slate-50">
        <div className="flex items-center space-x-3 text-emerald-600">
          <div className="w-2.5 h-2.5 bg-emerald-500 rounded-full animate-ping"></div>
          <span className="text-[10px] font-black uppercase tracking-widest">IA Conectada</span>
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
    const t = localStorage.getItem("rv_tutores");
    const p = localStorage.getItem("rv_pets");
    const r = localStorage.getItem("rv_records");
    if (t) setTutores(JSON.parse(t));
    if (p) setPets(JSON.parse(p));
    if (r) setRecords(JSON.parse(r));
  }, []);

  useEffect(() => {
    localStorage.setItem("rv_tutores", JSON.stringify(tutores));
    localStorage.setItem("rv_pets", JSON.stringify(pets));
    localStorage.setItem("rv_records", JSON.stringify(records));
  }, [tutores, pets, records]);

  const addTutor = (t: Omit<Tutor, "id">) => setTutores(prev => [...prev, { ...t, id: crypto.randomUUID() }]);
  const addPet = (p: Pet) => { setPets(prev => [...prev, p]); setActivePetId(p.id); };
  const addRecord = (r: Omit<MedicalRecord, "id">) => setRecords(prev => [...prev, { ...r, id: crypto.randomUUID() }]);
  const restore = (data: any) => {
    setTutores(data.tutores || []);
    setPets(data.pets || []);
    setRecords(data.records || data.historico || []);
  };

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar currentTab={currentTab} setTab={setCurrentTab} />
      <main className="flex-1 ml-64 p-12 max-w-6xl mx-auto w-full">
        {currentTab === AppTab.TUTORES && <TutorView tutores={tutores} onAdd={addTutor} onGoToPets={() => setCurrentTab(AppTab.PETS)} />}
        {currentTab === AppTab.PETS && <PetView pets={pets} tutores={tutores} onAdd={addPet} onGoToTutores={() => setCurrentTab(AppTab.TUTORES)} onGoToProntuario={(id) => { setActivePetId(id); setCurrentTab(AppTab.PRONTUARIO); }} />}
        {currentTab === AppTab.PRONTUARIO && <ProntuarioView pets={pets} records={records} onAdd={addRecord} onGoToPets={() => setCurrentTab(AppTab.PETS)} selectedId={activePetId} onSelect={setActivePetId} />}
        {currentTab === AppTab.BACKUP && <BackupView data={{ tutores, pets, records }} onRestore={restore} />}
      </main>
    </div>
  );
}

// --- Views Internas ---

const TutorView: React.FC<{ tutores: Tutor[], onAdd: (t: Omit<Tutor, "id">) => void, onGoToPets: () => void }> = ({ tutores, onAdd, onGoToPets }) => {
  const [f, setF] = useState({ nome: "", cpf: "", tel: "", email: "", endereco: "" });
  const [msg, setMsg] = useState(false);

  return (
    <div className="space-y-10 animate-fadeIn">
      <header><h2 className="text-4xl font-black text-slate-800">Tutores</h2></header>
      {msg && <div className="bg-emerald-600 text-white p-6 rounded-3xl font-bold flex justify-between items-center shadow-lg animate-bounce"><span>✅ Cadastro realizado!</span><button onClick={onGoToPets} className="bg-white text-emerald-600 px-6 py-2 rounded-xl text-xs font-black">ADICIONAR PET</button></div>}
      <form onSubmit={e => { e.preventDefault(); onAdd({...f, nome: f.nome.toUpperCase()}); setF({nome:"", cpf:"", tel:"", email:"", endereco:""}); setMsg(true); setTimeout(()=>setMsg(false), 5000); }} className="bg-white p-12 rounded-[50px] shadow-2xl border border-white space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <input placeholder="NOME DO TUTOR *" required className="p-6 bg-slate-50 rounded-3xl outline-none focus:ring-4 focus:ring-blue-100 font-bold" value={f.nome} onChange={e => setF({...f, nome: e.target.value})} />
          <input placeholder="CPF *" required className="p-6 bg-slate-50 rounded-3xl outline-none focus:ring-4 focus:ring-blue-100 font-bold" value={f.cpf} onChange={e => setF({...f, cpf: e.target.value})} />
          <input placeholder="WhatsApp" className="p-6 bg-slate-50 rounded-3xl outline-none" value={f.tel} onChange={e => setF({...f, tel: e.target.value})} />
          <input placeholder="E-mail" className="p-6 bg-slate-50 rounded-3xl outline-none" value={f.email} onChange={e => setF({...f, email: e.target.value})} />
          <input placeholder="Endereço" className="md:col-span-2 p-6 bg-slate-50 rounded-3xl outline-none" value={f.endereco} onChange={e => setF({...f, endereco: e.target.value})} />
        </div>
        <button className="w-full bg-blue-600 text-white py-6 rounded-3xl font-black text-xl hover:bg-blue-700 shadow-xl transition-all">SALVAR TUTOR</button>
      </form>
    </div>
  );
};

const PetView: React.FC<{ pets: Pet[], tutores: Tutor[], onAdd: (p: Pet) => void, onGoToTutores: () => void, onGoToProntuario: (id: string) => void }> = ({ pets, tutores, onAdd, onGoToTutores, onGoToProntuario }) => {
  const [f, setF] = useState({ nome: "", raca: "", nascimento: "", tutorId: "" });
  if (tutores.length === 0) return <div className="text-center py-32 bg-white rounded-[50px] shadow-sm border-2 border-dashed border-slate-200 flex flex-col items-center"><div>⚠️</div><h3 className="mt-4 font-black">Cadastre um tutor primeiro</h3><button onClick={onGoToTutores} className="mt-6 bg-blue-600 text-white px-10 py-4 rounded-2xl font-black">IR PARA TUTORES</button></div>;

  return (
    <div className="space-y-10 animate-fadeIn">
      <header><h2 className="text-4xl font-black text-slate-800">Pacientes</h2></header>
      <form onSubmit={(e) => { e.preventDefault(); onAdd({...f, id: crypto.randomUUID(), nome: f.nome.toUpperCase(), raca: f.raca.toUpperCase()}); setF({nome:"", raca:"", nascimento:"", tutorId:f.tutorId}); }} className="bg-white p-12 rounded-[50px] shadow-2xl border border-white space-y-6">
        <select required className="w-full p-6 bg-slate-50 rounded-3xl font-bold appearance-none outline-none focus:ring-4 focus:ring-blue-100" value={f.tutorId} onChange={e => setF({...f, tutorId: e.target.value})}>
          <option value="">Selecione o Responsável</option>
          {tutores.map(t => <option key={t.id} value={t.id}>{t.nome}</option>)}
        </select>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <input placeholder="Nome do Pet *" required className="p-6 bg-slate-50 rounded-3xl font-bold" value={f.nome} onChange={e => setF({...f, nome: e.target.value})} />
          <input placeholder="Raça" className="p-6 bg-slate-50 rounded-3xl font-bold" value={f.raca} onChange={e => setF({...f, raca: e.target.value})} />
        </div>
        <button className="w-full bg-blue-600 text-white py-6 rounded-3xl font-black text-xl shadow-xl">CADASTRAR PACIENTE</button>
      </form>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {pets.map(p => (
          <div key={p.id} className="bg-white p-8 rounded-[40px] shadow-lg hover:shadow-2xl transition-all group border border-slate-100">
            <h4 className="font-black text-2xl text-slate-800">{p.nome}</h4>
            <p className="text-xs font-black text-blue-600 uppercase tracking-widest mb-6">{p.raca || "Raça indefinida"}</p>
            <button onClick={() => onGoToProntuario(p.id)} className="w-full py-4 bg-slate-900 text-white rounded-2xl font-black text-xs hover:bg-blue-600 transition-colors flex items-center justify-center space-x-2"><Icons.Record /><span>PRONTUÁRIO</span></button>
          </div>
        ))}
      </div>
    </div>
  );
};

const ProntuarioView: React.FC<{ pets: Pet[], records: MedicalRecord[], onAdd: (r: Omit<MedicalRecord, "id">) => void, onGoToPets: () => void, selectedId: string, onSelect: (id: string) => void }> = ({ pets, records, onAdd, onGoToPets, selectedId, onSelect }) => {
  const [sin, setSin] = useState("");
  const [obs, setObs] = useState("");
  const [load, setLoad] = useState(false);
  const [ai, setAi] = useState("");

  const voice = (field: 'sin' | 'obs', text: string) => {
    if (field === 'sin') setSin(p => p ? `${p} ${text}` : text);
    else setObs(p => p ? `${p} ${text}` : text);
  };

  const selectedPet = pets.find(p => p.id === selectedId);

  return (
    <div className="space-y-12 pb-32 animate-fadeIn">
      <header><h2 className="text-4xl font-black text-slate-800 tracking-tight">Atendimento</h2></header>
      <div className="bg-white p-12 rounded-[60px] shadow-2xl border border-white space-y-12">
        <select className="w-full p-8 bg-slate-50 rounded-[40px] font-black text-2xl border-none focus:ring-8 focus:ring-blue-50 text-slate-800 shadow-inner appearance-none cursor-pointer text-center" value={selectedId} onChange={e => { onSelect(e.target.value); setAi(""); }}>
          <option value="">Escolha o Paciente</option>
          {pets.map(p => <option key={p.id} value={p.id}>{p.nome} ({p.raca})</option>)}
        </select>

        {selectedId && (
          <div className="space-y-12 animate-fadeIn">
            <div className="space-y-4">
              <div className="flex justify-between items-center px-4"><label className="text-xs font-black text-slate-400 uppercase tracking-widest">Anamnese / Sintomas</label><VoiceButton onResult={(t)=>voice('sin', t)} /></div>
              <textarea className="w-full p-10 bg-slate-50 rounded-[45px] min-h-[200px] outline-none focus:bg-white focus:ring-4 focus:ring-blue-50 text-xl font-medium shadow-inner" placeholder="O que o pet está apresentando?" value={sin} onChange={e => setSin(e.target.value)} />
              <button onClick={async () => { if(!sin || !selectedPet) return; setLoad(true); const res = await getAiDiagnosisSuggestion(sin, {nome:selectedPet.nome, raca:selectedPet.raca}); setAi(res || ""); setLoad(false); }} disabled={load || !sin} className="flex items-center space-x-3 bg-blue-50 text-blue-700 px-10 py-5 rounded-3xl font-black hover:bg-blue-100 transition-all shadow-sm">
                <Icons.Sparkles /> <span>{load ? "IA ANALISANDO..." : "CONSULTAR IA VETERINÁRIA"}</span>
              </button>
            </div>

            {ai && (
              <div className="bg-gradient-to-br from-blue-800 to-blue-900 p-12 rounded-[50px] text-white shadow-2xl animate-slideUp leading-relaxed relative overflow-hidden">
                <div className="flex items-center space-x-2 mb-6 font-black border-b border-white/20 pb-4 text-xs uppercase tracking-widest opacity-80"><Icons.AI /><span>Sugestão Pro AI</span></div>
                <div className="whitespace-pre-wrap text-xl opacity-90">{ai}</div>
              </div>
            )}

            <div className="space-y-4">
              <div className="flex justify-between items-center px-4"><label className="text-xs font-black text-slate-400 uppercase tracking-widest">Conduta / Tratamento</label><VoiceButton onResult={(t)=>voice('obs', t)} /></div>
              <textarea className="w-full p-10 bg-slate-50 rounded-[45px] min-h-[200px] outline-none focus:bg-white focus:ring-4 focus:ring-blue-50 text-xl font-medium shadow-inner" placeholder="Plano de tratamento..." value={obs} onChange={e => setObs(e.target.value)} />
            </div>

            <button onClick={() => { onAdd({ petId: selectedId, data: new Date().toLocaleDateString("pt-BR"), observacoes: obs, sintomas: sin, diagnosticoAi: ai }); setSin(""); setObs(""); setAi(""); alert("Salvo!"); }} className="w-full bg-slate-900 text-white py-8 rounded-[40px] font-black text-2xl uppercase tracking-[4px] shadow-2xl hover:scale-[1.01] transition-all">FINALIZAR CONSULTA</button>
          </div>
        )}
      </div>

      <div className="space-y-8 mt-20 px-4">
        <h3 className="font-black text-3xl text-slate-800">Histórico Médico</h3>
        <div className="space-y-8">
          {records.filter(r => r.petId === selectedId).reverse().map(r => (
            <div key={r.id} className="bg-white p-12 rounded-[55px] border border-slate-100 shadow-xl flex flex-col md:flex-row gap-12">
              <div className="flex-shrink-0"><span className="text-[10px] font-black text-blue-600 bg-blue-50 px-6 py-2 rounded-full uppercase tracking-widest">{r.data}</span></div>
              <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-10">
                <div className="space-y-2"><p className="font-black text-slate-300 uppercase text-[9px] tracking-widest border-b pb-2">Anamnese</p><p className="text-slate-700 text-lg leading-relaxed">{r.sintomas || "-"}</p></div>
                <div className="space-y-2"><p className="font-black text-slate-300 uppercase text-[9px] tracking-widest border-b pb-2">Conduta</p><p className="text-slate-700 text-lg leading-relaxed font-bold">{r.observacoes || "-"}</p></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const BackupView: React.FC<{ data: any, onRestore: (d: any) => void }> = ({ data, onRestore }) => (
  <div className="space-y-12 animate-fadeIn">
    <header><h2 className="text-4xl font-black text-slate-800">Dados</h2></header>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
      <button onClick={() => { const b = new Blob([JSON.stringify(data, null, 2)], {type:"application/json"}); const u = URL.createObjectURL(b); const a = document.createElement("a"); a.href = u; a.download = `VET_BACKUP_${new Date().getTime()}.json`; a.click(); }} className="bg-white p-20 rounded-[60px] shadow-xl flex flex-col items-center space-y-8 group hover:shadow-2xl transition-all">
        <div className="w-24 h-24 bg-emerald-50 text-emerald-600 rounded-[35px] flex items-center justify-center text-4xl group-hover:scale-110 transition-transform"><Icons.Backup /></div>
        <div className="text-center"><h4 className="font-black text-2xl text-slate-800 uppercase tracking-tighter">Baixar Base</h4><p className="text-slate-400 mt-2 font-bold">Cria um arquivo de segurança.</p></div>
      </button>
      <div className="relative bg-white p-20 rounded-[60px] shadow-xl flex flex-col items-center space-y-8 group hover:shadow-2xl transition-all cursor-pointer">
        <input type="file" className="absolute inset-0 opacity-0 cursor-pointer z-10" onChange={(e) => { const f = e.target.files?.[0]; if(!f) return; const r = new FileReader(); r.onload=(ev) => { try { onRestore(JSON.parse(ev.target?.result as string)); alert("Banco restaurado!"); } catch { alert("Erro no arquivo."); } }; r.readAsText(f); }} />
        <div className="w-24 h-24 bg-amber-50 text-amber-600 rounded-[35px] flex items-center justify-center text-4xl group-hover:scale-110 transition-transform">⚠️</div>
        <div className="text-center"><h4 className="font-black text-2xl text-slate-800 uppercase tracking-tighter">Restaurar</h4><p className="text-slate-400 mt-2 font-bold">Recupera dados salvos.</p></div>
      </div>
    </div>
  </div>
);
