
import React, { useState, useEffect } from 'react';
import { Tutor, Pet, MedicalRecord, AppTab } from './types';
import { getAiDiagnosisSuggestion } from './services/geminiService';

// --- Helper Components ---

const Sidebar: React.FC<{ 
  currentTab: AppTab; 
  setTab: (tab: AppTab) => void 
}> = ({ currentTab, setTab }) => {
  const menuItems = [
    { id: AppTab.TUTORES, icon: '👤', label: 'Tutores' },
    { id: AppTab.PETS, icon: '🐾', label: 'Pets' },
    { id: AppTab.PRONTUARIO, icon: '📋', label: 'Prontuário' },
    { id: AppTab.BACKUP, icon: '💾', label: 'Backup' },
  ];

  return (
    <div className="w-64 bg-white border-r h-screen flex flex-col fixed left-0 top-0 z-10">
      <div className="p-6 border-b flex items-center space-x-2">
        <span className="text-3xl">🐾</span>
        <h1 className="text-xl font-bold text-slate-800">Ribeira Vet</h1>
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setTab(item.id)}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-colors ${
              currentTab === item.id
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span className="font-medium">{item.label}</span>
          </button>
        ))}
      </nav>
      <div className="p-4 border-t text-xs text-slate-400 text-center">
        v2.1 Pro AI - © 2024
      </div>
    </div>
  );
};

export default function App() {
  const [currentTab, setCurrentTab] = useState<AppTab>(AppTab.TUTORES);
  const [tutores, setTutores] = useState<Tutor[]>([]);
  const [pets, setPets] = useState<Pet[]>([]);
  const [records, setRecords] = useState<MedicalRecord[]>([]);

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
    setPets(prev => [...prev, { ...p, id: crypto.randomUUID() }]);
  };

  const addRecord = (r: Omit<MedicalRecord, 'id'>) => {
    setRecords(prev => [...prev, { ...r, id: crypto.randomUUID() }]);
  };

  const restoreBackup = (data: any) => {
    if (data.tutores) setTutores(data.tutores);
    if (data.pets) setPets(data.pets);
    if (data.records) setRecords(data.records || data.historico || []);
  };

  return (
    <div className="flex min-h-screen">
      <Sidebar currentTab={currentTab} setTab={setCurrentTab} />
      
      <main className="flex-1 ml-64 p-8 max-w-5xl mx-auto w-full">
        {currentTab === AppTab.TUTORES && (
          <TutorView tutores={tutores} onAdd={addTutor} onGoToPets={() => setCurrentTab(AppTab.PETS)} />
        )}
        {currentTab === AppTab.PETS && (
          <PetView pets={pets} tutores={tutores} onAdd={addPet} onGoToTutores={() => setCurrentTab(AppTab.TUTORES)} onGoToProntuario={() => setCurrentTab(AppTab.PRONTUARIO)} />
        )}
        {currentTab === AppTab.PRONTUARIO && (
          <ProntuarioView pets={pets} records={records} onAdd={addRecord} onGoToPets={() => setCurrentTab(AppTab.PETS)} />
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
        <h2 className="text-3xl font-bold text-slate-800">👤 Cadastro de Tutores</h2>
        <p className="text-slate-500">Gerencie os proprietários dos pacientes.</p>
      </header>

      {justAdded && (
        <div className="bg-green-100 border border-green-200 text-green-800 p-4 rounded-xl flex justify-between items-center animate-bounce">
          <span>✅ Tutor cadastrado com sucesso! Deseja cadastrar o pet agora?</span>
          <button onClick={onGoToPets} className="bg-green-600 text-white px-4 py-1 rounded-lg font-bold text-sm">CADASTRAR PET ➡️</button>
        </div>
      )}

      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-2xl shadow-sm border space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="md:col-span-1">
            <label className="block text-sm font-medium text-slate-700 mb-1">Nome do Tutor *</label>
            <input
              type="text"
              required
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              value={form.nome}
              onChange={e => setForm({ ...form, nome: e.target.value })}
              placeholder="EX: JOÃO DA SILVA"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">CPF *</label>
            <input
              type="text"
              required
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              value={form.cpf}
              onChange={e => setForm({ ...form, cpf: e.target.value })}
              placeholder="000.000.000-00"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">WhatsApp</label>
            <input
              type="text"
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              value={form.tel}
              onChange={e => setForm({ ...form, tel: e.target.value })}
              placeholder="(00) 00000-0000"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">E-mail</label>
            <input
              type="email"
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              value={form.email}
              onChange={e => setForm({ ...form, email: e.target.value })}
              placeholder="email@exemplo.com"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-slate-700 mb-1">Endereço</label>
            <input
              type="text"
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              value={form.endereco}
              onChange={e => setForm({ ...form, endereco: e.target.value })}
              placeholder="Rua, número, bairro..."
            />
          </div>
        </div>
        <button type="submit" className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700 transition shadow-lg">
          💾 SALVAR TUTOR
        </button>
      </form>

      <div className="bg-white rounded-2xl shadow-sm border overflow-hidden">
        <table className="w-full text-left text-sm md:text-base">
          <thead className="bg-slate-50 border-b">
            <tr>
              <th className="px-6 py-4 text-sm font-semibold text-slate-600">Nome</th>
              <th className="px-6 py-4 text-sm font-semibold text-slate-600">CPF</th>
              <th className="px-6 py-4 text-sm font-semibold text-slate-600">Contato</th>
              <th className="px-6 py-4 text-sm font-semibold text-slate-600">Endereço</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {tutores.map(t => (
              <tr key={t.id} className="hover:bg-slate-50">
                <td className="px-6 py-4 font-medium text-slate-800">{t.nome}</td>
                <td className="px-6 py-4 text-slate-600 font-mono text-xs">{t.cpf}</td>
                <td className="px-6 py-4 text-slate-600">
                  {t.tel} <br /> <span className="text-xs text-slate-400">{t.email}</span>
                </td>
                <td className="px-6 py-4 text-slate-600">{t.endereco}</td>
              </tr>
            ))}
            {tutores.length === 0 && (
              <tr>
                <td colSpan={4} className="px-6 py-10 text-center text-slate-400 italic">Nenhum tutor cadastrado.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const PetView: React.FC<{ 
  pets: Pet[], 
  tutores: Tutor[], 
  onAdd: (p: Omit<Pet, 'id'>) => void,
  onGoToTutores: () => void,
  onGoToProntuario: () => void
}> = ({ pets, tutores, onAdd, onGoToTutores, onGoToProntuario }) => {
  const [form, setForm] = useState({ nome: '', raca: '', nascimento: '', tutorId: '' });
  const [justAdded, setJustAdded] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.nome || !form.tutorId) return;
    onAdd({ 
      ...form, 
      nome: form.nome.toUpperCase(),
      raca: form.raca.toUpperCase()
    });
    setForm({ nome: '', raca: '', nascimento: '', tutorId: '' });
    setJustAdded(true);
    setTimeout(() => setJustAdded(false), 5000);
  };

  if (tutores.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center space-y-4 py-20 bg-white rounded-3xl border shadow-sm">
        <span className="text-6xl">⚠️</span>
        <h3 className="text-xl font-bold text-slate-800">Nenhum Tutor Cadastrado</h3>
        <p className="text-slate-500 max-w-sm text-center">Para cadastrar um Pet, você precisa primeiro cadastrar um Tutor.</p>
        <button onClick={onGoToTutores} className="bg-blue-600 text-white px-8 py-3 rounded-xl font-bold shadow-lg">
          Ir para Cadastro de Tutores
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fadeIn">
      <header>
        <h2 className="text-3xl font-bold text-slate-800">🐾 Cadastro de Pacientes</h2>
        <p className="text-slate-500">Registre os pets e vincule aos seus donos.</p>
      </header>

      {justAdded && (
        <div className="bg-blue-100 border border-blue-200 text-blue-800 p-4 rounded-xl flex justify-between items-center animate-bounce">
          <span>✅ Pet cadastrado! Vamos abrir o prontuário para este paciente?</span>
          <button onClick={onGoToProntuario} className="bg-blue-600 text-white px-4 py-1 rounded-lg font-bold text-sm">ABRIR PRONTUÁRIO 📋</button>
        </div>
      )}

      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-2xl shadow-sm border space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-slate-700 mb-1">Selecione o Tutor *</label>
            <select
              required
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              value={form.tutorId}
              onChange={e => setForm({ ...form, tutorId: e.target.value })}
            >
              <option value="">--- Selecione um Tutor ---</option>
              {tutores.map(t => (
                <option key={t.id} value={t.id}>{t.nome} (CPF: {t.cpf})</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Nome do Pet *</label>
            <input
              type="text"
              required
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              value={form.nome}
              onChange={e => setForm({ ...form, nome: e.target.value })}
              placeholder="EX: LUNA"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Raça</label>
            <input
              type="text"
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              value={form.raca}
              onChange={e => setForm({ ...form, raca: e.target.value })}
              placeholder="EX: GOLDEN RETRIEVER"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Data de Nascimento</label>
            <input
              type="text"
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              value={form.nascimento}
              onChange={e => setForm({ ...form, nascimento: e.target.value })}
              placeholder="DD/MM/AAAA"
            />
          </div>
        </div>
        <button type="submit" className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700 transition shadow-lg">
          💾 SALVAR PACIENTE
        </button>
      </form>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {pets.map(p => {
          const tutor = tutores.find(t => t.id === p.tutorId);
          return (
            <div key={p.id} className="bg-white p-5 rounded-2xl border shadow-sm flex items-start space-x-4">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-2xl flex-shrink-0">
                🐶
              </div>
              <div>
                <h4 className="font-bold text-slate-800">{p.nome}</h4>
                <p className="text-xs text-slate-500 uppercase font-semibold">{p.raca || 'Raça não inf.'}</p>
                <div className="mt-2 text-sm text-slate-600">
                  <span className="font-medium">Tutor:</span> {tutor?.nome || 'Desconhecido'}
                </div>
                <div className="text-xs text-slate-400 mt-1">Nasc: {p.nascimento || '--/--/----'}</div>
              </div>
            </div>
          );
        })}
        {pets.length === 0 && (
          <div className="col-span-full py-10 text-center text-slate-400 italic">Nenhum pet cadastrado.</div>
        )}
      </div>
    </div>
  );
};

const ProntuarioView: React.FC<{ 
  pets: Pet[], 
  records: MedicalRecord[],
  onAdd: (r: Omit<MedicalRecord, 'id'>) => void,
  onGoToPets: () => void 
}> = ({ pets, records, onAdd, onGoToPets }) => {
  const [selectedPetId, setSelectedPetId] = useState('');
  const [sintomas, setSintomas] = useState('');
  const [observacoes, setObservacoes] = useState('');
  const [isAiLoading, setIsAiLoading] = useState(false);
  const [aiSuggestion, setAiSuggestion] = useState('');

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
    alert('Prontuário salvo!');
  };

  if (pets.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center space-y-4 py-20 bg-white rounded-3xl border shadow-sm">
        <span className="text-6xl">📋</span>
        <h3 className="text-xl font-bold text-slate-800">Prontuário Vazio</h3>
        <p className="text-slate-500 max-w-sm text-center">Para abrir um prontuário, você precisa primeiro ter um Pet cadastrado.</p>
        <button onClick={onGoToPets} className="bg-blue-600 text-white px-8 py-3 rounded-xl font-bold shadow-lg">
          Ir para Cadastro de Pets
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fadeIn pb-20">
      <header>
        <h2 className="text-3xl font-bold text-slate-800">📋 Prontuário Médico</h2>
        <p className="text-slate-500">Histórico de consultas e auxílio diagnóstico por IA.</p>
      </header>

      <div className="bg-white p-6 rounded-2xl shadow-sm border space-y-6">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">Selecione o Paciente para Iniciar</label>
          <select
            className="w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 outline-none text-lg"
            value={selectedPetId}
            onChange={e => {
              setSelectedPetId(e.target.value);
              setAiSuggestion('');
            }}
          >
            <option value="">--- Clique aqui para selecionar o Pet ---</option>
            {pets.map(p => (
              <option key={p.id} value={p.id}>{p.nome} ({p.raca})</option>
            ))}
          </select>
        </div>

        {selectedPetId && (
          <div className="space-y-6 pt-4 border-t border-slate-100">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Queixa Principal / Sintomas</label>
              <textarea
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none min-h-[100px]"
                placeholder="Descreva o que o pet está sentindo..."
                value={sintomas}
                onChange={e => setSintomas(e.target.value)}
              />
              <button
                type="button"
                onClick={handleAiConsult}
                disabled={isAiLoading || !sintomas}
                className="mt-2 flex items-center space-x-2 text-blue-600 font-semibold hover:text-blue-800 disabled:text-slate-400"
              >
                <span>✨</span>
                <span>{isAiLoading ? 'Analisando com IA...' : 'Consultar Sugestão da IA'}</span>
              </button>
            </div>

            {aiSuggestion && (
              <div className="bg-blue-50 border border-blue-100 p-4 rounded-xl text-sm text-slate-700 whitespace-pre-wrap">
                <div className="flex items-center space-x-2 mb-2 font-bold text-blue-800">
                  <span>🤖</span> <span>Sugestão Clínica (IA):</span>
                </div>
                {aiSuggestion}
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Conduta e Observações Finais</label>
              <textarea
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none min-h-[100px]"
                placeholder="Tratamento, medicamentos, recomendações..."
                value={observacoes}
                onChange={e => setObservacoes(e.target.value)}
              />
            </div>

            <button
              onClick={handleSubmit}
              className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700 shadow-lg"
            >
              💾 SALVAR PRONTUÁRIO
            </button>
          </div>
        )}
      </div>

      <div className="space-y-4">
        <h3 className="text-xl font-bold text-slate-800">Histórico de Consultas</h3>
        {selectedPetId ? (
          <div className="space-y-4">
            {records.filter(r => r.petId === selectedPetId).reverse().map(r => (
              <div key={r.id} className="bg-white p-6 rounded-2xl border shadow-sm">
                <div className="flex justify-between items-center mb-4">
                  <span className="bg-slate-100 text-slate-600 px-3 py-1 rounded-full text-xs font-bold">{r.data}</span>
                </div>
                <div className="space-y-3">
                  <div>
                    <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Sintomas</h5>
                    <p className="text-slate-700">{r.sintomas || 'Não informado'}</p>
                  </div>
                  <div>
                    <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Conduta Veterinária</h5>
                    <p className="text-slate-700">{r.observacoes || 'Sem observações'}</p>
                  </div>
                  {r.diagnosticoAi && (
                    <div className="pt-3 border-t border-slate-50">
                      <h5 className="text-xs font-bold text-blue-400 uppercase tracking-wider">Auxílio IA</h5>
                      <p className="text-slate-500 text-sm italic">{r.diagnosticoAi.substring(0, 200)}...</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
            {records.filter(r => r.petId === selectedPetId).length === 0 && (
              <p className="text-center text-slate-400 py-10">Nenhum histórico encontrado para este paciente.</p>
            )}
          </div>
        ) : (
          <div className="text-center py-10 bg-slate-50 rounded-2xl border-2 border-dashed text-slate-400">
            Selecione um paciente para ver o histórico.
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
        <h2 className="text-3xl font-bold text-slate-800">💾 Backup e Segurança</h2>
        <p className="text-slate-500">Exporte seus dados ou restaure uma cópia de segurança.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-8 rounded-3xl border shadow-sm flex flex-col items-center text-center space-y-4">
          <div className="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-3xl">
            📥
          </div>
          <h3 className="text-xl font-bold text-slate-800">Exportar Dados</h3>
          <p className="text-slate-500 text-sm">Crie uma cópia de segurança de todos os tutores, pets e prontuários cadastrados.</p>
          <button
            onClick={downloadBackup}
            className="w-full bg-green-600 text-white py-3 rounded-xl font-bold hover:bg-green-700 transition"
          >
            BAIXAR BACKUP (.JSON)
          </button>
        </div>

        <div className="bg-white p-8 rounded-3xl border shadow-sm flex flex-col items-center text-center space-y-4">
          <div className="w-16 h-16 bg-amber-100 text-amber-600 rounded-full flex items-center justify-center text-3xl">
            🔄
          </div>
          <h3 className="text-xl font-bold text-slate-800">Restaurar Dados</h3>
          <p className="text-slate-500 text-sm">Importe um arquivo de backup anterior para restaurar as informações.</p>
          <div className="w-full relative">
            <input
              type="file"
              accept=".json,.txt"
              onChange={handleFileUpload}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
            <div className="bg-amber-600 text-white py-3 rounded-xl font-bold hover:bg-amber-700 transition pointer-events-none">
              SELECIONAR ARQUIVO
            </div>
          </div>
        </div>
      </div>
      
      <div className="bg-blue-50 border border-blue-100 p-6 rounded-2xl text-blue-800 text-sm">
        <h4 className="font-bold mb-2 flex items-center space-x-2">
          <span>💡</span> <span>Dica de Segurança</span>
        </h4>
        <p>
          Os dados são salvos automaticamente no seu navegador, mas é recomendável baixar um backup semanalmente 
          para evitar perda de dados em caso de limpeza de cache ou troca de computador.
        </p>
      </div>
    </div>
  );
};
