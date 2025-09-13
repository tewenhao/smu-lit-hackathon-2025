'use client'

import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { ArrowLeft, Brain, Search, Building, AlertTriangle, CheckCircle } from 'lucide-react'

interface Agent {
  name: string
  icon: React.ReactNode
  role: string
  className: string
}

interface AgentAnalysis {
  thought: string
  output: string
}

const agents: Agent[] = [
  {
    name: 'Researcher',
    icon: <Search className="w-5 h-5" />,
    role: 'Legal Research & Precedent Analysis',
    className: 'border-l-emerald-500'
  },
  {
    name: 'Case Builder',
    icon: <Building className="w-5 h-5" />,
    role: 'Argument Structure & Evidence Organization',
    className: 'border-l-blue-500'
  },
  {
    name: 'Concluder',
    icon: <CheckCircle className="w-5 h-5" />,
    role: 'Strategic Synthesis & Final Recommendations',
    className: 'border-l-purple-500'
  },
  {
    name: 'Weakness Identifier',
    icon: <AlertTriangle className="w-5 h-5" />,
    role: 'Risk Assessment & Vulnerability Analysis',
    className: 'border-l-amber-500'
  },
]

const formatOutput = (text: string): string => {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>')
}

const LoadingOverlay = () => (
  <div className="fixed inset-0 bg-white/90 backdrop-blur-sm flex items-center justify-center z-50">
    <Card className="w-80">
      <CardContent className="pt-6">
        <div className="text-center space-y-4">
          <div className="w-12 h-12 border-4 border-gray-200 border-t-blue-500 rounded-full animate-spin mx-auto" />
          <div>
            <p className="font-semibold text-gray-900">AI Agents Analyzing Your Case</p>
            <p className="text-sm text-gray-600">This may take a few moments...</p>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
)

const AgentCard = ({ 
  agent, 
  analysis, 

}: { 
  agent: Agent
  analysis: AgentAnalysis

}) => {
  const [isVisible, setIsVisible] = useState(true)

  return (
    <Card 
      className={`transition-all duration-500 transform ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-5'
      } hover:shadow-lg hover:-translate-y-1 border-l-4 ${agent.className}`}
    >
      <CardHeader className="pb-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
            {agent.icon}
          </div>
          <div>
            <CardTitle className="text-base">{agent.name}</CardTitle>
            <CardDescription className="text-xs">{agent.role}</CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Label className="text-xs text-gray-500 uppercase tracking-wide font-semibold">
            Thought Process
          </Label>
          <div className="mt-1 p-3 bg-gray-50 rounded-lg border-l-2 border-gray-200">
            <p className="text-sm text-gray-600 italic leading-relaxed">
              {analysis.output}
            </p>
          </div>
        </div>
        <div>
          <Label className="text-xs text-gray-500 uppercase tracking-wide font-semibold">
            Analysis Output
          </Label>
          <div 
            className="mt-1 text-sm text-gray-700 leading-relaxed"
            dangerouslySetInnerHTML={{ __html: formatOutput(analysis.output) }}
          />
        </div>
      </CardContent>
    </Card>
  )
}

interface Report {
  "user_context": string, 
  "user_prompt": string, 
  "final_report": string
}

export default function ArbitrationAnalyzer() {
  const [currentView, setCurrentView] = useState<'input' | 'results'>('input')
  const [isLoading, setIsLoading] = useState(false)
  const [caseScenario, setCaseScenario] = useState('')
  const [userPrompt, setUserPrompt] = useState('')
  const [analyses, setAnalyses] = useState<AgentAnalysis[]>([])
  const [report, setReport] = useState<Report>()

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!caseScenario.trim() || !userPrompt.trim()) {
      alert('Please fill in both the case scenario and your specific question.')
      return
    }

    setIsLoading(true)
    
    const payload = { 
      "context":caseScenario,
      "prompt": userPrompt, 
      "tone": "professional"
    }
    // Simulate API processing time
    const response = await fetch('http://127.0.0.1:8000/generate/result', {
      method: "POST", 
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    }).then(response => {return response})
    
    
    // Generate analyses 
    await response.json().then(object => {
      const tempA: AgentAnalysis[] = []
      for (const key in object.thoughts) {
        tempA.push(object.thoughts[key])
      }
      setAnalyses(tempA)
      setReport({
        user_context: object.user_context, 
        user_prompt: object.user_prompt, 
        final_report: object.final_report
      })
    })

    setIsLoading(false)
    setCurrentView('results')
  }

  const handleNewAnalysis = () => {
    setCurrentView('input')
    setCaseScenario('')
    setUserPrompt('')
    setAnalyses([])
  }

  if (currentView === 'input') {
    return (
      <>
        {isLoading && <LoadingOverlay />}
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-2xl">
            <CardHeader className="text-center space-y-4">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl flex items-center justify-center mx-auto">
                <span className="text-2xl">⚖️</span>
              </div>
              <div>
                <CardTitle className="text-2xl font-bold">Sigma Tech AI Assistant</CardTitle>
                <CardDescription className="text-base mt-2">
                  Provide your case details below and our AI agents will analyze your arbitration scenario from multiple perspectives
                </CardDescription>
              </div>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleAnalyze} className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="scenario">Case Scenario & Background</Label>
                  <Textarea
                    id="scenario"
                    value={caseScenario}
                    onChange={(e) => setCaseScenario(e.target.value)}
                    placeholder="Describe the dispute, key events, timeline, parties involved, and any relevant contract terms or agreements..."
                    className="min-h-[120px]"
                    required
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="prompt">Specific Question or Analysis Request</Label>
                  <Textarea
                    id="prompt"
                    value={userPrompt}
                    onChange={(e) => setUserPrompt(e.target.value)}
                    placeholder="What specific analysis do you need? e.g., 'Assess the strength of our breach of contract claim and potential damages' or 'Identify risks and develop arbitration strategy'"
                    className="min-h-[120px]"
                    required
                  />
                </div>
                
                <Button type="submit" className="w-full" size="lg" disabled={isLoading}>
                  <Brain className="w-5 h-5 mr-2" />
                  Analyze Case with AI Agents
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Button
        variant="outline"
        onClick={handleNewAnalysis}
        className="fixed top-4 left-4 z-40"
      >
        <ArrowLeft className="w-4 h-4 mr-2" />
        New Analysis
      </Button>

      <div className="max-w-7xl mx-auto p-4">
        <Card className="mb-6">
          <CardHeader className="text-center bg-gradient-to-r from-gray-50 to-gray-100">
            <CardTitle className="text-2xl font-bold">AI Agent Analysis Complete</CardTitle>
            <CardDescription>
              Our specialized AI agents have analyzed your case from multiple perspectives
            </CardDescription>
            <Card className="mt-4 bg-blue-50 border-blue-200">
              <CardContent className="pt-4">
                <div className="text-left">
                  <Label className="text-xs text-gray-600 uppercase tracking-wide font-semibold">
                    Case Summary
                  </Label>
                  <p className="mt-1 text-sm text-gray-800">
                    <strong>Commercial Arbitration Case Analysis</strong><br />
                    {report?.user_context.substring(0, 200)}{report!.user_context.length > 200 ? '...' : ''}
                  </p>
                </div>
              </CardContent>
            </Card>
          </CardHeader>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {agents.map((agent, index) => (
            <AgentCard
              key={agent.name}
              agent={agent}
              analysis={analyses[index]}
            />
          ))}
          
        </div>

        {/* ------ final report -----  */}
          <div className='py-4'>
            <Card>
              <CardHeader>
                Final case report
              </CardHeader>
              <CardContent>
                {report?.final_report}
              </CardContent>
            </Card>
          </div>
      </div>
    </div>
  )
}