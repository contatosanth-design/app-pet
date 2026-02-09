
import React, { useState, useEffect } from 'react';
import { Tutor, Pet, MedicalRecord, AppTab } from './types';
import { getAiDiagnosisSuggestion } from './services/geminiService';

// --- Icons (SVG to avoid "invalid character" errors in some environments) ---
const Icons = {
  Tutor: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>,
  Pet: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>,
  Record: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>,
  Backup: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" /></svg>,
  AI: () => <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 10-2 0v1a1 1 0 102 0v-1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 10-2 0v1a1 1 0 102 0v-1zM8 16v-1a1 1 0 10-2 0v1a1 1 0 102 0zM12 16v-1a1 1 0 10-2 0v1a1 1 0 102 0zM16 16v-1a1 1 0 10-2 0v1a1 1 0 102 0z" /></svg>
};

// --- Helper Components ---

const Sidebar: React.FC<{ 
  currentTab: AppTab; 
  setTab: (tab: AppTab) => void 
}> = ({ currentTab, setTab }) => {
  const menuItems = [
    { id: AppTab.TUTORES, icon: <Icons.Tutor />, label: 'Tutores' },
    { id: AppTab.PETS, icon: <Icons.Pet />, label: 'Pets' },
    { id: AppTab.PRONTUARIO, icon: <Icons.Record />, label: 'Prontuário' },
    { id: AppTab.BACKUP, icon: <Icons.Backup />, label: 'Backup' },
  ];

  return (
    <div className="w-64 bg-white border-r h-screen flex flex-col fixed left-0 top-0 z-10">
      <div className="p-6 border-b flex items-center space-x-2">
        <div className="text-blue-600 font-bold text-2xl">RV</div>
        <h1 className="text-xl font-bold text-slate-800">Ribeira Vet</h1>
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setTab(item.id)}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 ${
              currentTab === item.id
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-200'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            {item.icon}
            <span className="font-semibold">{item.label}</span>
          </button>
        ))}
      </nav>
      <div className="p-4 border-t text-[10px] text-slate-400 text-center uppercase tracking-widest font-bold">
        v2.5 Pro AI &copy; 2024
      </div>
    </div>
  );
};

export default function App() {
  const [currentTab, setCurrentTab] = useState<AppTab>(AppTab.TUTORES);
  const [tutores, setTutores] = useState<Tutor[]>([]);
  const [pets, setPets] = useState<Pet[]>([]);
  const [records, setRecords] = useState<MedicalRecord[]>([]);
  const [activePetId, setActivePetId] = useState<string>('');

  // LocalStorage Sync
  useEffect(() => {
    const savedTutores = localStorage.getItem('rv_tutores');
    const savedPets = localStorage.getItem('rv_pets');
    const savedRecords = localStorage.getItem('rv_records');
    if (savedTutores) setTutores(JSON.parse(savedTutores));
    if (savedPets) setPets(JSON.parse(savedPets));
    if (savedRecords) setRecords(JSON.parse(savedRecords));
  }, []);

  useEffect(() => {
    localStorage.setItem('rv_tutores', JSON.stringify(tutores));
    localStorage.setItem('rv_pets', JSON.stringify(pets));
    localStorage.setItem('rv_records', JSON.stringify(records));
  }, [tutores, pets, records]);

  // Actions
  const addTutor = (t: Omit<Tutor, 'id'>) => {
    setTutores(prev => [...prev, { ...t, id: crypto.randomUUID() }]);
  };

  const addPet = (p: Omit<Pet, 'id'>) => {
    const id = crypto.randomUUID();
    setPets(prev => [...prev, { ...p, id }]);
    setActivePetId(id); // Set active pet for the record flow
  };

  const addRecord = (r: Omit<MedicalRecord, 'id'>) => {
    setRecords(prev => [...prev, { ...r, id: crypto.randomUUID() }]);
  };

  const restoreBackup = (data: any) => {
    if (data.tutores) setTutores(data.tutores);
    if (data.pets) setPets(data.pets);
    if (data.records) setRecords(data.records || data.historico || []);
  };

  const navigateToProntuario = (petId?: string) => {
    if (petId) setActivePetId(petId);
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
          <PetView 
            pets={pets} 
            tutores={tutores} 
            onAdd={addPet} 
            onGoToTutores={() => setCurrentTab(AppTab.TUTORES)} 
            onGoToProntuario={navigateToProntuario} 
          />
        )}
        {currentTab === AppTab.PRONTUARIO && (
          <ProntuarioView 
            pets={pets} 
            records={records} 
            onAdd={addRecord} 
            onGoToPets={() => setCurrentTab(AppTab.PETS)} 
            initialPetId={activePetId}
            onPetChange={setActivePetId}
          />
        )}
        {currentTab === AppTab.BACKUP && (
          <BackupView 
            data={{ tutores, pets, records }} 
            onRestore={restoreBackup} 
          />
        )}
      </main>
    </div>
  );
}

// --- View Components ---

const TutorView: React.FC<{ tutores: Tutor[], onAdd: (t: Omit<Tutor, 'id'>) => void, onGoToPets: () => void }> = ({ tutores, onAdd, onGoToPets }) => {
  const [form, setForm] = useState({ nome: '', cpf: '', tel: '', email: '', endereco: '' });
  const [justAdded, setJustAdded] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.nome || !form.cpf) return;
    onAdd({ ...form, nome: form.nome.toUpperCase() });
    setForm({ nome: '', cpf: '', tel: '', email: '', endereco: '' });
    setJustAdded(true);
    setTimeout(() => setJustAdded(false), 5000);
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      <header>
        <h2 className="text-3xl font-bold text-slate-800">Cadastro de Tutores</h2>
        <p className="text-slate-500 font-medium">Gerencie os proprietários dos pacientes.</p>
      </header>

      {justAdded && (
        <div className="bg-green-50 border border-green-200 text-green-800 p-4 rounded-2xl flex justify-between items-center shadow-sm">
          <span className="font-semibold">✓ Tutor cadastrado com sucesso!</span>
          <button onClick={onGoToPets} className="bg-green-600 text-white px-4 py-2 rounded-xl font-bold text-sm hover:bg-green-700 transition-colors flex items-center space-x-2">
            <span>CADASTRAR PET</span>
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
          </button>
        </div>
      )}

      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="md:col-span-1">
            <label className="block text-xs font-bold text-slate-400 uppercase mb-2">Nome do Tutor *</label>
            <input
              type="text"
              required
              className="w-full px-4 py-3 bg-slate-50 border border-transparent rounded-xl focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              value={form.nome}
              onChange={e => setForm({ ...form, nome: e.target.value })}
              placeholder="EX: JOÃO DA SILVA"
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-400 uppercase mb-2">CPF *</label>
            <input
              type="text"
              required
              className="w-full px-4 py-3 bg-slate-50 border border-transparent rounded-xl focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              value={form.cpf}
              onChange={e => setForm({ ...form, cpf: e.target.value })}
              placeholder="000.000.000-00"
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-400 uppercase mb-2">WhatsApp</label>
            <input
              type="text"
              className="w-full px-4 py-3 bg-slate-50 border border-transparent rounded-xl focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              value={form.tel}
              onChange={e => setForm({ ...form, tel: e.target.value })}
              placeholder="(00) 00000-0000"
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-400 uppercase mb-2">E-mail</label>
            <input
              type="email"
              className="w-full px-4 py-3 bg-slate-50 border border-transparent rounded-xl focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              value={form.email}
              onChange={e => setForm({ ...form, email: e.target.value })}
              placeholder="email@exemplo.com"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-xs font-bold text-slate-400 uppercase mb-2">Endereço</label>
            <input
              type="text"
              className="w-full px-4 py-3 bg-slate-50 border border-transparent rounded-xl focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              value={form.endereco}
              onChange={e => setForm({ ...form, endereco: e.target.value })}
              placeholder="Rua, número, bairro..."
            />
          </div>
        </div>
        <button type="submit" className="w-full bg-blue-600 text-white py-4 rounded-2xl font-bold hover:bg-blue-700 transition shadow-xl shadow-blue-100 flex items-center justify-center space-x-2">
          <span>SALVAR TUTOR</span>
        </button>
      </form>

      <div className="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-slate-50/50 border-b border-slate-100">
              <tr>
                <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Nome</th>
                <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">CPF</th>
                <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Contato</th>
                <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Endereço</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-50">
              {tutores.map(t => (
                <tr key={t.id} className="hover:bg-slate-50/80 transition-colors">
                  <td className="px-6 py-4 font-bold text-slate-800">{t.nome}</td>
                  <td className="px-6 py-4 text-slate-500 font-mono text-xs bg-slate-50/30">{t.cpf}</td>
                  <td className="px-6 py-4 text-slate-600">
                    <div className="font-semibold">{t.tel}</div>
                    <div className="text-xs text-slate-400">{t.email}</div>
                  </td>
                  <td className="px-6 py-4 text-slate-500 text-sm">{t.endereco}</td>
                </tr>
              ))}
              {tutores.length === 0 && (
                <tr>
                  <td colSpan={4} className="px-6 py-12 text-center text-slate-400 italic font-medium">Nenhum tutor cadastrado no sistema.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const PetView: React.FC<{ 
  pets: Pet[], 
  tutores: Tutor[], 
  onAdd: (p: Omit<Pet, 'id'>) => void,
  onGoToTutores: () => void,
  onGoToProntuario: (id: string) => void
}> = ({ pets, tutores, onAdd, onGoToTutores, onGoToProntuario }) => {
  const [form, setForm] = useState({ nome: '', raca: '', nascimento: '', tutorId: '' });
  const [lastPetId, setLastPetId] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.nome || !form.tutorId) return;
    const newPetId = crypto.randomUUID();
    onAdd({ 
      ...form, 
      nome: form.nome.toUpperCase(),
      raca: form.raca.toUpperCase()
    });
    setForm({ nome: '', raca: '', nascimento: '', tutorId: '' });
    setLastPetId(newPetId); // Actually addPet updates state, but we'll show success
  };

  if (tutores.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center space-y-6 py-24 bg-white rounded-[40px] border border-slate-100 shadow-sm text-center">
        <div className="w-24 h-24 bg-amber-50 rounded-full flex items-center justify-center text-amber-500">
          <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
        </div>
        <div>
          <h3 className="text-2xl font-bold text-slate-800 mb-2">Nenhum Tutor Cadastrado</h3>
          <p className="text-slate-500 max-w-sm mx-auto">Cadastre primeiro um proprietário antes de adicionar um paciente.</p>
        </div>
        <button onClick={onGoToTutores} className="bg-blue-600 text-white px-10 py-4 rounded-2xl font-bold shadow-xl shadow-blue-100 hover:bg-blue-700 transition-all">
          CADASTRAR TUTOR AGORA
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fadeIn">
      <header>
        <h2 className="text-3xl font-bold text-slate-800">Cadastro de Pacientes</h2>
        <p className="text-slate-500 font-medium">Registre os pets e vincule aos seus donos.</p>
      </header>

      {lastPetId && (
        <div className="bg-blue-50 border border-blue-100 p-5 rounded-3xl flex justify-between items-center shadow-sm animate-pulse-once">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center">✓</div>
            <span className="font-bold text-blue-900">Pet cadastrado com sucesso!</span>
          </div>
          <button 
            onClick={() => onGoToProntuario('')} 
            className="bg-blue-600 text-white px-6 py-2.5 rounded-2xl font-bold text-sm hover:bg-blue-700 transition flex items-center space-x-2"
          >
            <span>ABRIR PRONTUÁRIO</span>
            <Icons.Record />
          </button>
        </div>
      )}

      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="md:col-span-2">
            <label className="block text-xs font-bold text-slate-400 uppercase mb-2">Selecione o Tutor *</label>
            <select
              required
              className="w-full px-4 py-3 bg-slate-50 border border-transparent rounded-xl focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all cursor-pointer"
              value={form.tutorId}
              onChange={e => setForm({ ...form, tutorId: e.target.value })}
            >
              <option value="">--- Clique para selecionar o proprietário ---</option>
              {tutores.map(t => (
                <option key={t.id} value={t.id}>{t.nome} (CPF: {t.cpf})</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-400 uppercase mb-2">Nome do Paciente *</label>
            <input
              type="text"
              required
              className="w-full px-4 py-3 bg-slate-50 border border-transparent rounded-xl focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              value={form.nome}
              onChange={e => setForm({ ...form, nome: e.target.value })}
              placeholder="EX: LUNA"
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-400 uppercase mb-2">Raça</label>
            <input
              type="text"
              className="w-full px-4 py-3 bg-slate-50 border border-transparent rounded-xl focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              value={form.raca}
              onChange={e => setForm({ ...form, raca: e.target.value })}
              placeholder="EX: GOLDEN RETRIEVER"
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-400 uppercase mb-2">Data de Nascimento</label>
            <input
              type="text"
              className="w-full px-4 py-3 bg-slate-50 border border-transparent rounded-xl focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              value={form.nascimento}
              onChange={e => setForm({ ...form, nascimento: e.target.value })}
              placeholder="DD/MM/AAAA"
            />
          </div>
        </div>
        <button type="submit" className="w-full bg-blue-600 text-white py-4 rounded-2xl font-bold hover:bg-blue-700 transition-all shadow-xl shadow-blue-50">
          SALVAR PACIENTE
        </button>
      </form>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {pets.map(p => {
          const tutor = tutores.find(t => t.id === p.tutorId);
          return (
            <div key={p.id} className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow cursor-default group">
              <div className="flex items-start space-x-4">
                <div className="w-14 h-14 bg-blue-50 text-blue-500 rounded-2xl flex items-center justify-center text-2xl group-hover:bg-blue-600 group-hover:text-white transition-all">
                  🐶
                </div>
                <div>
                  <h4 className="font-bold text-slate-800 text-lg leading-tight">{p.nome}</h4>
                  <p className="text-[10px] text-slate-400 uppercase font-bold tracking-wider mb-2">{p.raca || 'Raça não inf.'}</p>
                  <div className="text-xs text-slate-600">
                    <span className="text-slate-400 font-medium">Tutor:</span> {tutor?.nome || 'Desconhecido'}
                  </div>
                </div>
              </div>
              <div className="mt-6 flex justify-between items-center">
                <div className="text-[10px] text-slate-300 font-bold uppercase tracking-tighter">Nasc: {p.nascimento || '--/--/----'}</div>
                <button 
                  onClick={() => onGoToProntuario(p.id)}
                  className="p-2 text-blue-600 hover:bg-blue-50 rounded-xl transition-colors"
                  title="Abrir Prontuário"
                >
                  <Icons.Record />
                </button>
              </div>
            </div>
          );
        })}
        {pets.length === 0 && (
          <div className="col-span-full py-16 text-center text-slate-300 font-medium italic border-2 border-dashed border-slate-100 rounded-3xl">Nenhum pet cadastrado.</div>
        )}
      </div>
    </div>
  );
};

const ProntuarioView: React.FC<{ 
  pets: Pet[], 
  records: MedicalRecord[],
  onAdd: (r: Omit<MedicalRecord, 'id'>) => void,
  onGoToPets: () => void,
  initialPetId?: string,
  onPetChange: (id: string) => void
}> = ({ pets, records, onAdd, onGoToPets, initialPetId, onPetChange }) => {
  const [selectedPetId, setSelectedPetId] = useState(initialPetId || '');
  const [sintomas, setSintomas] = useState('');
  const [observacoes, setObservacoes] = useState('');
  const [isAiLoading, setIsAiLoading] = useState(false);
  const [aiSuggestion, setAiSuggestion] = useState('');

  // Sincroniza com o pet ativo se houver mudança externa (ex: navegação)
  useEffect(() => {
    if (initialPetId) setSelectedPetId(initialPetId);
  }, [initialPetId]);

  const selectedPet = pets.find(p => p.id === selectedPetId);

  const handleAiConsult = async () => {
    if (!sintomas || !selectedPet) return;
    setIsAiLoading(true);
    const suggestion = await getAiDiagnosisSuggestion(sintomas, { nome: selectedPet.nome, raca: selectedPet.raca });
    setAiSuggestion(suggestion || '');
    setIsAiLoading(false);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedPetId) return;
    onAdd({
      petId: selectedPetId,
      data: new Date().toLocaleDateString('pt-BR'),
      observacoes,
      sintomas,
      diagnosticoAi: aiSuggestion
    });
    setSintomas('');
    setObservacoes('');
    setAiSuggestion('');
    alert('Consulta registrada com sucesso!');
  };

  if (pets.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center space-y-6 py-24 bg-white rounded-[40px] border border-slate-100 shadow-sm text-center">
        <div className="w-24 h-24 bg-blue-50 rounded-full flex items-center justify-center text-blue-500">
          <Icons.Record />
        </div>
        <div>
          <h3 className="text-2xl font-bold text-slate-800 mb-2">Prontuário Vazio</h3>
          <p className="text-slate-500 max-w-sm mx-auto">Não há pacientes cadastrados. Adicione um pet para começar os registros médicos.</p>
        </div>
        <button onClick={onGoToPets} className="bg-blue-600 text-white px-10 py-4 rounded-2xl font-bold shadow-xl shadow-blue-100 hover:bg-blue-700 transition-all">
          CADASTRAR PET AGORA
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fadeIn pb-24">
      <header>
        <h2 className="text-3xl font-bold text-slate-800">Prontuário Médico</h2>
        <p className="text-slate-500 font-medium">Histórico de consultas e inteligência artificial veterinária.</p>
      </header>

      <div className="bg-white p-8 rounded-[32px] shadow-sm border border-slate-100 space-y-8">
        <div>
          <label className="block text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">Selecione o Paciente</label>
          <select
            className="w-full px-5 py-4 bg-slate-50 border border-transparent rounded-2xl focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-lg font-bold text-slate-700 transition-all cursor-pointer"
            value={selectedPetId}
            onChange={e => {
              const id = e.target.value;
              setSelectedPetId(id);
              onPetChange(id);
              setAiSuggestion('');
            }}
          >
            <option value="">--- Selecionar Paciente para consulta ---</option>
            {pets.map(p => (
              <option key={p.id} value={p.id}>{p.nome} ({p.raca})</option>
            ))}
          </select>
        </div>

        {selectedPetId && (
          <div className="space-y-8 animate-fadeIn">
            <div className="bg-slate-50/50 p-6 rounded-3xl border border-slate-100 flex items-center space-x-4">
              <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center text-xl shadow-sm">🐶</div>
              <div>
                <h4 className="font-bold text-slate-800">Atendimento: {selectedPet?.nome}</h4>
                <p className="text-xs text-slate-400 font-bold uppercase tracking-wider">{selectedPet?.raca}</p>
              </div>
            </div>

            <div className="space-y-4">
              <label className="block text-xs font-bold text-slate-400 uppercase tracking-widest">Sintomas e Observações Clínicas</label>
              <textarea
                className="w-full px-5 py-4 bg-slate-50 border border-transparent rounded-2xl focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none min-h-[140px] text-slate-700 transition-all"
                placeholder="Ex: Vômitos, falta de apetite, letargia há 2 dias..."
                value={sintomas}
                onChange={e => setSintomas(e.target.value)}
              />
              <button
                type="button"
                onClick={handleAiConsult}
                disabled={isAiLoading || !sintomas}
                className="flex items-center space-x-3 px-6 py-3 bg-blue-50 text-blue-700 rounded-2xl font-bold text-sm hover:bg-blue-100 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
              >
                <div className={`${isAiLoading ? 'animate-spin' : 'group-hover:animate-bounce'}`}>
                   {isAiLoading ? '...' : '✨'}
                </div>
                <span>{isAiLoading ? 'Processando Sintomas...' : 'Consultar Diagnóstico IA'}</span>
              </button>
            </div>

            {aiSuggestion && (
              <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-3xl text-white shadow-xl shadow-blue-100 animate-slideUp">
                <div className="flex items-center space-x-2 mb-4">
                  <div className="p-2 bg-white/20 rounded-lg"><Icons.AI /></div>
                  <h4 className="font-bold text-lg">Sugestão Clínica Pro AI</h4>
                </div>
                <div className="text-sm leading-relaxed opacity-90 whitespace-pre-wrap font-medium">
                  {aiSuggestion}
                </div>
                <div className="mt-4 pt-4 border-t border-white/10 text-[10px] uppercase font-bold tracking-widest opacity-60">
                  Assistente Virtual de Decisão Clínica
                </div>
              </div>
            )}

            <div className="space-y-4">
              <label className="block text-xs font-bold text-slate-400 uppercase tracking-widest">Conduta Veterinária Final</label>
              <textarea
                className="w-full px-5 py-4 bg-slate-50 border border-transparent rounded-2xl focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none min-h-[100px] text-slate-700 transition-all"
                placeholder="Prescrição, exames solicitados, retorno..."
                value={observacoes}
                onChange={e => setObservacoes(e.target.value)}
              />
            </div>

            <button
              onClick={handleSubmit}
              className="w-full bg-slate-900 text-white py-5 rounded-2xl font-bold hover:bg-black transition-all shadow-2xl shadow-slate-200 uppercase tracking-widest text-sm"
            >
              Finalizar e Salvar Registro
            </button>
          </div>
        )}
      </div>

      <div className="space-y-6">
        <h3 className="text-xl font-bold text-slate-800 px-2 flex items-center space-x-2">
           <Icons.Record />
           <span>Histórico Recente</span>
        </h3>
        {selectedPetId ? (
          <div className="space-y-4">
            {records.filter(r => r.petId === selectedPetId).reverse().map(r => (
              <div key={r.id} className="bg-white p-8 rounded-[32px] border border-slate-100 shadow-sm hover:border-blue-200 transition-colors group">
                <div className="flex justify-between items-center mb-6">
                  <div className="bg-blue-50 text-blue-600 px-4 py-1.5 rounded-full text-xs font-bold">{r.data}</div>
                  <div className="text-slate-200 group-hover:text-blue-100 transition-colors"><Icons.Record /></div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div>
                    <h5 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">Anamnese / Sintomas</h5>
                    <p className="text-slate-700 font-medium leading-relaxed">{r.sintomas || 'Nenhum sintoma relatado.'}</p>
                  </div>
                  <div>
                    <h5 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">Conduta Veterinária</h5>
                    <p className="text-slate-700 font-medium leading-relaxed">{r.observacoes || 'Nenhuma conduta registrada.'}</p>
                  </div>
                </div>
                {r.diagnosticoAi && (
                  <div className="mt-6 pt-6 border-t border-slate-50">
                    <h5 className="text-[10px] font-bold text-blue-300 uppercase tracking-widest mb-2">Suporte IA Utilizado</h5>
                    <p className="text-slate-400 text-xs italic line-clamp-2">{r.diagnosticoAi}</p>
                  </div>
                )}
              </div>
            ))}
            {records.filter(r => r.petId === selectedPetId).length === 0 && (
              <div className="text-center py-20 bg-slate-50/50 rounded-[32px] border border-dashed border-slate-100 text-slate-400 font-medium italic">
                Ainda não há consultas registradas para {selectedPet?.nome}.
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-24 bg-slate-50/30 rounded-[40px] border-2 border-dashed border-slate-100 text-slate-300 font-bold uppercase tracking-widest text-xs">
            Selecione um paciente para carregar o histórico médico
          </div>
        )}
      </div>
    </div>
  );
};

const BackupView: React.FC<{ data: any, onRestore: (data: any) => void }> = ({ data, onRestore }) => {
  const downloadBackup = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `backup_ribeira_vet_${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const json = JSON.parse(event.target?.result as string);
        onRestore(json);
        alert('Dados restaurados com sucesso!');
      } catch (err) {
        alert('Erro ao processar o arquivo. Verifique se o formato está correto.');
      }
    };
    reader.readAsText(file);
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      <header>
        <h2 className="text-3xl font-bold text-slate-800">Centro de Segurança</h2>
        <p className="text-slate-500 font-medium">Exporte seus dados ou restaure uma cópia de segurança.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white p-10 rounded-[40px] border border-slate-100 shadow-sm flex flex-col items-center text-center space-y-6 group hover:shadow-xl transition-all duration-300">
          <div className="w-20 h-20 bg-green-50 text-green-500 rounded-3xl flex items-center justify-center text-4xl group-hover:scale-110 transition-transform duration-300">
            <Icons.Backup />
          </div>
          <div>
            <h3 className="text-xl font-bold text-slate-800 mb-2">Exportar Nuvem Local</h3>
            <p className="text-slate-400 text-sm max-w-xs font-medium">Baixe todos os tutores, pets e registros em um único arquivo seguro.</p>
          </div>
          <button
            onClick={downloadBackup}
            className="w-full bg-green-600 text-white py-4 rounded-2xl font-bold hover:bg-green-700 transition shadow-lg shadow-green-100"
          >
            GERAR ARQUIVO DE BACKUP
          </button>
        </div>

        <div className="bg-white p-10 rounded-[40px] border border-slate-100 shadow-sm flex flex-col items-center text-center space-y-6 group hover:shadow-xl transition-all duration-300">
          <div className="w-20 h-20 bg-amber-50 text-amber-500 rounded-3xl flex items-center justify-center text-4xl group-hover:scale-110 transition-transform duration-300">
            <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
          </div>
          <div>
            <h3 className="text-xl font-bold text-slate-800 mb-2">Restaurar Sistema</h3>
            <p className="text-slate-400 text-sm max-w-xs font-medium">Recupere informações de um arquivo gerado anteriormente.</p>
          </div>
          <div className="w-full relative">
            <input
              type="file"
              accept=".json,.txt"
              onChange={handleFileUpload}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
            />
            <div className="bg-amber-600 text-white py-4 rounded-2xl font-bold hover:bg-amber-700 transition shadow-lg shadow-amber-100 pointer-events-none">
              SELECIONAR BACKUP
            </div>
          </div>
        </div>
      </div>
      
      <div className="bg-slate-900 p-8 rounded-[32px] text-white shadow-2xl shadow-slate-200">
        <h4 className="font-bold mb-4 flex items-center space-x-3 text-blue-400">
          <Icons.AI /> <span>Protocolo de Segurança Ribeira Vet</span>
        </h4>
        <div className="space-y-4 text-sm font-medium opacity-80 leading-relaxed">
          <p>• Seus dados são armazenados localmente no navegador (LocalStorage).</p>
          <p>• Limpar o histórico do navegador pode remover os dados se não houver backup.</p>
          <p>• Recomendamos exportar seus dados ao final de cada expediente.</p>
        </div>
      </div>
    </div>
  );
};
