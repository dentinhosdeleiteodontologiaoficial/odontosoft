import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Calendar, Users, DollarSign, FileText, MessageSquare, Plus } from 'lucide-react'
import './App.css'

// Importações adicionais para o modal de agendamento
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog.jsx'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover.jsx'
import { format } from 'date-fns'
import { ptBR } from 'date-fns/locale' // Importe o locale para português do Brasil
import { cn } from '@/lib/utils.js' // Importe a função cn para classes condicionais
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Calendar as CalendarIcon } from 'lucide-react' // Renomeie para evitar conflito com Calendar do shadcn/ui

// URL do backend - ajuste conforme necessário
const API_BASE_URL = 'https://odontosoft-backend.onrender.com' // Use a sua URL real do backend no Render

function App( ) {
  const [activeTab, setActiveTab] = useState('dashboard')

  const [patients, setPatients] = useState([])
  const [appointments, setAppointments] = useState([])
  const [budgets, setBudgets] = useState([])
  const [newPatient, setNewPatient] = useState({ 
    name: '', 
    phone: '', 
    email: '',
    responsible_name: '',
    responsible_phone: ''
  })

  // Estados para o modal de agendamento
  const [isAppointmentModalOpen, setIsAppointmentModalOpen] = useState(false)
  const [newAppointment, setNewAppointment] = useState({
    patient_id: '',
    start_time: null, // Usaremos Date objects aqui
    end_time: null,   // Usaremos Date objects aqui
    notes: '',
    treatment_type: '' // Campo para o assunto/tipo de tratamento
  })

  const addPatient = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/patients`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newPatient),
      })
      
      if (response.ok) {
        const result = await response.json()
        alert('Paciente adicionado com sucesso!')
        setNewPatient({ 
          name: '', 
          phone: '', 
          email: '',
          responsible_name: '',
          responsible_phone: ''
        })
        loadPatients() // Recarregar lista de pacientes
      } else {
        // Se a resposta não for OK, tente ler a mensagem de erro do backend
        const errorData = await response.json();
        alert(`Erro ao adicionar paciente: ${errorData.message || response.statusText}`);
      }
    } catch (error) {
      console.error('Erro ao adicionar paciente:', error)
      alert('Erro ao adicionar paciente')
    }
  }

  const loadPatients = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/patients`)
      if (response.ok) {
        const data = await response.json()
        setPatients(data.patients)
      }
    } catch (error) {
      console.error('Erro ao carregar pacientes:', error)
    }
  }

  const loadAppointments = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/appointments`)
      if (response.ok) {
        const data = await response.json()
        setAppointments(data.appointments)
      }
    } catch (error) {
      console.error('Erro ao carregar agendamentos:', error)
    }
  }

  const loadBudgets = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/budgets`)
      if (response.ok) {
        const data = await response.json()
        setBudgets(data.budgets)
      }
    } catch (error) {
      console.error('Erro ao carregar orçamentos:', error)
    }
  }

  const sendConfirmation = async (appointmentId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/whatsapp/send-confirmation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ appointment_id: appointmentId }),
      })
      
      if (response.ok) {
        const result = await response.json()
        alert('Confirmação enviada via WhatsApp!')
      } else {
        const errorData = await response.json();
        alert(`Erro ao enviar confirmação: ${errorData.message || response.statusText}`);
      }
    } catch (error) {
      console.error('Erro ao enviar confirmação:', error)
      alert('Erro ao enviar confirmação')
    }
  }

  // Função para adicionar agendamento
  const addAppointment = async () => {
    try {
      // Validação básica
      if (!newAppointment.patient_id || !newAppointment.start_time || !newAppointment.end_time) {
        alert('Por favor, preencha todos os campos obrigatórios: Paciente, Data e Horário.')
        return
      }

      // Formatar as datas para ISO string antes de enviar para o backend
      const formattedAppointment = {
        ...newAppointment,
        start_time: newAppointment.start_time.toISOString(),
        end_time: newAppointment.end_time.toISOString(),
      }

      const response = await fetch(`${API_BASE_URL}/appointments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formattedAppointment),
      })
      
      if (response.ok) {
        const result = await response.json()
        alert('Agendamento adicionado com sucesso!')
        setIsAppointmentModalOpen(false) // Fechar modal
        setNewAppointment({ // Resetar formulário
          patient_id: '',
          start_time: null,
          end_time: null,
          notes: '',
          treatment_type: ''
        })
        loadAppointments() // Recarregar lista de agendamentos
      } else {
        const errorData = await response.json();
        alert(`Erro ao adicionar agendamento: ${errorData.message || response.statusText}`);
      }
    } catch (error) {
      console.error('Erro ao adicionar agendamento:', error)
      alert('Erro ao adicionar agendamento')
    }
  }

  // Carregar dados ao inicializar
  useEffect(() => {
    loadPatients()
    loadAppointments()
    loadBudgets()
  }, [])

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-blue-600 mb-2">OdontoSoft</h1>
          <p className="text-gray-600">Sistema de Gestão Odontológica - Odontopediatria</p>
        </header>

        {/* Adicione as propriedades value e onValueChange para controlar a aba */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="dashboard" className="flex items-center gap-2">
              <DollarSign className="w-4 h-4" />
              Dashboard
            </TabsTrigger>
            <TabsTrigger value="patients" className="flex items-center gap-2">
              <Users className="w-4 h-4" />
              Pacientes
            </TabsTrigger>
            <TabsTrigger value="appointments" className="flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              Agenda
            </TabsTrigger>
            <TabsTrigger value="financial" className="flex items-center gap-2">
              <FileText className="w-4 h-4" />
              Financeiro
            </TabsTrigger>
            <TabsTrigger value="whatsapp" className="flex items-center gap-2">
              <MessageSquare className="w-4 h-4" />
              WhatsApp
            </TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total de Pacientes</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{patients.length}</div>
                  <p className="text-xs text-muted-foreground">Pacientes cadastrados</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Consultas Agendadas</CardTitle>
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{appointments.length}</div>
                  <p className="text-xs text-muted-foreground">Próximas consultas</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Orçamentos</CardTitle>
                  <FileText className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{budgets.length}</div>
                  <p className="text-xs text-muted-foreground">Orçamentos criados</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Faturamento Mensal</CardTitle>
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">R$ 0,00</div>
                  <p className="text-xs text-muted-foreground">Este mês</p>
                </CardContent>
              </Card>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card>
                <CardHeader>
                  <CardTitle>Próximas Consultas</CardTitle>
                </CardHeader>
                <CardContent>
                  {appointments.length === 0 ? (
                    <p className="text-gray-500">Nenhuma consulta agendada.</p>
                  ) : (
                    <div className="space-y-2">
                      {appointments.slice(0, 5).map((appointment) => (
                        <div key={appointment.id} className="flex justify-between items-center p-2 border rounded">
                          <div>
                            <p className="font-medium">{appointment.patient_name}</p>
                            <p className="text-sm text-gray-500">
                              {new Date(appointment.start_time).toLocaleString('pt-BR')}
                            </p>
                          </div>
                          <span className={`px-2 py-1 rounded text-xs ${
                            appointment.status === 'Confirmado' ? 'bg-green-100 text-green-800' :
                            appointment.status === 'Agendado' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {appointment.status}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Ações Rápidas</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  {/* Botão Novo Agendamento - abre o modal */}
                  <Button 
                    className="w-full justify-start" 
                    variant="outline"
                    onClick={() => {
                      setActiveTab('appointments'); // Opcional: muda para a aba de agendamentos
                      setIsAppointmentModalOpen(true); // Abre o modal
                    }} 
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Novo Agendamento
                  </Button>
                  {/* Botão Novo Orçamento - apenas muda a aba por enquanto */}
                  <Button 
                    className="w-full justify-start" 
                    variant="outline"
                    onClick={() => setActiveTab('financial')}
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Novo Orçamento
                  </Button>
                  {/* Botão Enviar Lembretes - apenas muda a aba por enquanto */}
                  <Button 
                    className="w-full justify-start" 
                    variant="outline"
                    onClick={() => setActiveTab('whatsapp')}
                  >
                    <MessageSquare className="w-4 h-4 mr-2" />
                    Enviar Lembretes
                  </Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="patients" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Cadastrar Novo Paciente</CardTitle>
                <CardDescription>Adicione um novo paciente ao sistema</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="name">Nome da Criança</Label>
                    <Input
                      id="name"
                      value={newPatient.name}
                      onChange={(e) => setNewPatient({...newPatient, name: e.target.value})}
                      placeholder="Digite o nome da criança"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="phone">Telefone da Criança</Label>
                    <Input
                      id="phone"
                      value={newPatient.phone}
                      onChange={(e) => setNewPatient({...newPatient, phone: e.target.value})}
                      placeholder="(11) 99999-9999"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email">E-mail</Label>
                    <Input
                      id="email"
                      type="email"
                      value={newPatient.email}
                      onChange={(e) => setNewPatient({...newPatient, email: e.target.value})}
                      placeholder="email@exemplo.com"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="responsible_name">Nome do Responsável</Label>
                    <Input
                      id="responsible_name"
                      value={newPatient.responsible_name}
                      onChange={(e) => setNewPatient({...newPatient, responsible_name: e.target.value})}
                      placeholder="Nome do pai/mãe/responsável"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="responsible_phone">Telefone do Responsável</Label>
                    <Input
                      id="responsible_phone"
                      value={newPatient.responsible_phone}
                      onChange={(e) => setNewPatient({...newPatient, responsible_phone: e.target.value})}
                      placeholder="(11) 99999-9999"
                    />
                  </div>
                </div>
                <Button onClick={addPatient} className="w-full md:w-auto">
                  <Plus className="w-4 h-4 mr-2" />
                  Cadastrar Paciente
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Lista de Pacientes</CardTitle>
                <CardDescription>Todos os pacientes cadastrados</CardDescription>
              </CardHeader>
              <CardContent>
                {patients.length === 0 ? (
                  <p className="text-gray-500">Nenhum paciente cadastrado ainda.</p>
                ) : (
                  <div className="space-y-2">
                    {patients.map((patient) => (
                      <div key={patient.id} className="flex justify-between items-center p-3 border rounded-lg">
                        <div>
                          <h3 className="font-medium">{patient.name}</h3>
                          <p className="text-sm text-gray-500">
                            {patient.phone} • {patient.email}
                          </p>
                          {patient.responsible_name && (
                            <p className="text-sm text-blue-600">
                              Responsável: {patient.responsible_name} • {patient.responsible_phone}
                            </p>
                          )}
                        </div>
                        <Button variant="outline" size="sm">
                          Ver Detalhes
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="appointments" className="space-y-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between">
                <div>
                  <CardTitle>Agenda de Consultas</CardTitle>
                  <CardDescription>Gerencie seus agendamentos</CardDescription>
                </div>
                {/* Botão Novo Agendamento na aba Agenda - abre o modal */}
                <Button onClick={() => setIsAppointmentModalOpen(true)}>
                  <Plus className="w-4 h-4 mr-2" />
                  Novo Agendamento
                </Button>
              </CardHeader>
              <CardContent>
                {appointments.length === 0 ? (
                  <p className="text-gray-500">Nenhuma consulta agendada.</p>
                ) : (
                  <div className="space-y-2">
                    {appointments.map((appointment) => (
                      <div key={appointment.id} className="flex justify-between items-center p-3 border rounded-lg">
                        <div>
                          <h3 className="font-medium">{patient.name}</h3>
                          <p className="text-sm text-gray-500">
                            {new Date(appointment.start_time).toLocaleString('pt-BR')} - 
                            {new Date(appointment.end_time).toLocaleString('pt-BR')}
                          </p>
                          {appointment.treatment_type && (
                            <p className="text-sm text-blue-600">Tipo: {appointment.treatment_type}</p>
                          )}
                        </div>
                        <div className="flex gap-2">
                          <span className={`px-2 py-1 rounded text-xs ${
                            appointment.status === 'Confirmado' ? 'bg-green-100 text-green-800' :
                            appointment.status === 'Agendado' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {appointment.status}
                          </span>
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => sendConfirmation(appointment.id)}
                          >
                            <MessageSquare className="w-4 h-4 mr-1" />
                            Confirmar
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="financial" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Controle Financeiro</CardTitle>
                <CardDescription>Orçamentos, pagamentos e faturamento</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Orçamentos</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">{budgets.length}</div>
                      <p className="text-sm text-gray-500">Total de orçamentos</p>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">A Receber</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">R$ 0,00</div>
                      <p className="text-sm text-gray-500">Pendente</p>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Recebido</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">R$ 0,00</div>
                      <p className="text-sm text-gray-500">Este mês</p>
                    </CardContent>
                  </Card>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="whatsapp" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Integração WhatsApp</CardTitle>
                <CardDescription>Gerencie mensagens e notificações automáticas</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Confirmações Automáticas</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-gray-600 mb-4">
                        Envie confirmações de consulta automaticamente 24h antes do agendamento.
                      </p>
                      <Button className="w-full">
                        <MessageSquare className="w-4 h-4 mr-2" />
                        Configurar Confirmações
                      </Button>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Lembretes de Retorno</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-gray-600 mb-4">
                        Configure lembretes automáticos para retornos e revisões.
                      </p>
                      <Button className="w-full">
                        <Calendar className="w-4 h-4 mr-2" />
                        Configurar Lembretes
                      </Button>
                    </CardContent>
                  </Card>
                </div>
                
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Status da Integração</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                      <span className="text-sm">Bot WhatsApp conectado e funcionando</span>
                    </div>
                    <p className="text-sm text-gray-600 mt-2">
                      Seu bot está pronto para enviar mensagens automáticas.
                    </p>
                  </CardContent>
                </Card>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>

      {/* Modal de Novo Agendamento */}
      <Dialog open={isAppointmentModalOpen} onOpenChange={setIsAppointmentModalOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Novo Agendamento</DialogTitle>
            <DialogDescription>
              Preencha os detalhes para agendar uma nova consulta.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            {/* Seleção de Paciente */}
            <div className="space-y-2">
              <Label htmlFor="patient">Paciente</Label>
              <Select
                onValueChange={(value) => setNewAppointment({ ...newAppointment, patient_id: value })}
                value={newAppointment.patient_id}
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Selecione um paciente" />
                </SelectTrigger>
                <SelectContent>
                  {patients.map((patient) => (
                    <SelectItem key={patient.id} value={patient.id.toString()}>
                      {patient.name} ({patient.responsible_name})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Seleção de Data */}
            <div className="space-y-2">
              <Label htmlFor="date">Data da Consulta</Label>
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant={"outline"}
                    className={cn(
                      "w-full justify-start text-left font-normal",
                      !newAppointment.start_time && "text-muted-foreground"
                    )}
                  >
                    <CalendarIcon className="mr-2 h-4 w-4" />
                    {newAppointment.start_time ? (
                      format(newAppointment.start_time, "PPP", { locale: ptBR })
                    ) : (
                      <span>Selecione uma data</span>
                    )}
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0">
                  <Calendar
                    mode="single"
                    selected={newAppointment.start_time}
                    onSelect={(date) => setNewAppointment({ ...newAppointment, start_time: date, end_time: date })} // Define a data de início e fim
                    initialFocus
                    locale={ptBR} // Define o locale para português do Brasil
                  />
                </PopoverContent>
              </Popover>
            </div>

            {/* Seleção de Horário */}
            <div className="space-y-2">
              <Label htmlFor="time">Horário da Consulta</Label>
              <Input
                id="time"
                type="time"
                value={newAppointment.start_time ? format(newAppointment.start_time, "HH:mm") : ""}
                onChange={(e) => {
                  const [hours, minutes] = e.target.value.split(':');
                  const date = newAppointment.start_time || new Date(); // Usa a data selecionada ou a data atual
                  date.setHours(parseInt(hours, 10));
                  date.setMinutes(parseInt(minutes, 10));
                  setNewAppointment({ ...newAppointment, start_time: date, end_time: date }); // Define a data de início e fim
                }}
              />
            </div>

            {/* Tipo de Tratamento (assunto) */}
            <div className="space-y-2">
              <Label htmlFor="treatment_type">Tipo de Tratamento / Assunto</Label>
              <Input
                id="treatment_type"
                value={newAppointment.treatment_type}
                onChange={(e) => setNewAppointment({ ...newAppointment, treatment_type: e.target.value })}
                placeholder="Ex: Limpeza, Restauração, Extração, Avaliação"
              />
            </div>

            {/* Notas (opcional) */}
            <div className="space-y-2">
              <Label htmlFor="notes">Notas</Label>
              <Input
                id="notes"
                value={newAppointment.notes}
                onChange={(e) => setNewAppointment({ ...newAppointment, notes: e.target.value })}
                placeholder="Observações sobre o agendamento"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsAppointmentModalOpen(false)}>Cancelar</Button>
            <Button onClick={addAppointment}>Salvar Agendamento</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

export default App
