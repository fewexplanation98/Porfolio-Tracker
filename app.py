import React, { useMemo, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Separator } from '@/components/ui/separator';
import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend, LineChart, Line } from 'recharts';
import { Wallet, TrendingUp, PiggyBank, PlusCircle, CheckCircle2, PencilLine, Euro, Activity } from 'lucide-react';

const assetsMaster = [
  { name: 'Core MSCI World', category: 'ETF', subcategory: 'ETF Stock', bucket: 'Stocks', pac: 640 },
  { name: 'AI & Big Data', category: 'ETF', subcategory: 'ETF Stock', bucket: 'Stocks', pac: 0 },
  { name: 'Physical Gold', category: 'ETF', subcategory: 'ETF Gold', bucket: 'Defensive', pac: 220 },
  { name: 'Global Gov Bond', category: 'ETF', subcategory: 'ETF Bond', bucket: 'Defensive', pac: 52 },
  { name: 'Core EUR Corp Bond', category: 'ETF', subcategory: 'ETF Bond', bucket: 'Defensive', pac: 54 },
  { name: 'MSCI World Value', category: 'ETF', subcategory: 'ETF Stock', bucket: 'Stocks', pac: 180 },
  { name: 'MSCI EM', category: 'ETF', subcategory: 'ETF Stock', bucket: 'Stocks', pac: 400 },
  { name: 'Defence Tech', category: 'ETF', subcategory: 'ETF Stock', bucket: 'Stocks', pac: 0 },
  { name: 'Savings', category: 'Savings', subcategory: 'Savings TR', bucket: 'Savings', pac: 0 },
];

const monthEndSeed = [
  { month: 'Oct/25', asset: 'Savings', value: 34010.01 },
  { month: 'Oct/25', asset: 'Core MSCI World', value: 11058 },
  { month: 'Oct/25', asset: 'AI & Big Data', value: 3265 },
  { month: 'Oct/25', asset: 'Physical Gold', value: 1792 },
  { month: 'Oct/25', asset: 'Global Gov Bond', value: 1456 },
  { month: 'Oct/25', asset: 'Core EUR Corp Bond', value: 1456 },
  { month: 'Oct/25', asset: 'MSCI World Value', value: 1439 },
  { month: 'Oct/25', asset: 'MSCI EM', value: 1233 },
  { month: 'Oct/25', asset: 'Defence Tech', value: 483.2 },
  { month: 'Nov/25', asset: 'Savings', value: 35690.22 },
  { month: 'Nov/25', asset: 'Core MSCI World', value: 11303 },
  { month: 'Nov/25', asset: 'AI & Big Data', value: 3177 },
  { month: 'Nov/25', asset: 'Physical Gold', value: 1875 },
  { month: 'Nov/25', asset: 'Global Gov Bond', value: 1470 },
  { month: 'Nov/25', asset: 'Core EUR Corp Bond', value: 1478 },
  { month: 'Nov/25', asset: 'MSCI World Value', value: 1499 },
  { month: 'Nov/25', asset: 'MSCI EM', value: 1225 },
  { month: 'Nov/25', asset: 'Defence Tech', value: 383.76 },
  { month: 'Dec/25', asset: 'Savings', value: 37889.16 },
  { month: 'Dec/25', asset: 'Core MSCI World', value: 11866 },
  { month: 'Dec/25', asset: 'AI & Big Data', value: 3256 },
  { month: 'Dec/25', asset: 'Physical Gold', value: 2001 },
  { month: 'Dec/25', asset: 'Global Gov Bond', value: 1547 },
  { month: 'Dec/25', asset: 'Core EUR Corp Bond', value: 1534 },
  { month: 'Dec/25', asset: 'MSCI World Value', value: 1651 },
  { month: 'Dec/25', asset: 'MSCI EM', value: 1306 },
  { month: 'Dec/25', asset: 'Defence Tech', value: 402.89 },
  { month: 'Jan/26', asset: 'Savings', value: 38095 },
  { month: 'Jan/26', asset: 'Core MSCI World', value: 12365 },
  { month: 'Jan/26', asset: 'AI & Big Data', value: 3215 },
  { month: 'Jan/26', asset: 'Physical Gold', value: 2214 },
  { month: 'Jan/26', asset: 'Global Gov Bond', value: 1568 },
  { month: 'Jan/26', asset: 'Core EUR Corp Bond', value: 1592 },
  { month: 'Jan/26', asset: 'MSCI World Value', value: 1824 },
  { month: 'Jan/26', asset: 'MSCI EM', value: 1419 },
  { month: 'Jan/26', asset: 'Defence Tech', value: 452.33 },
  { month: 'Feb/26', asset: 'Savings', value: 37801 },
  { month: 'Feb/26', asset: 'Core MSCI World', value: 13001 },
  { month: 'Feb/26', asset: 'AI & Big Data', value: 3108 },
  { month: 'Feb/26', asset: 'Physical Gold', value: 2540 },
  { month: 'Feb/26', asset: 'Global Gov Bond', value: 1640 },
  { month: 'Feb/26', asset: 'Core EUR Corp Bond', value: 1649 },
  { month: 'Feb/26', asset: 'MSCI World Value', value: 2007 },
  { month: 'Feb/26', asset: 'MSCI EM', value: 1544 },
  { month: 'Feb/26', asset: 'Defence Tech', value: 450.32 },
  { month: 'Mar/26', asset: 'Savings', value: 39883 },
  { month: 'Mar/26', asset: 'Core MSCI World', value: 13914 },
  { month: 'Mar/26', asset: 'AI & Big Data', value: 2970 },
  { month: 'Mar/26', asset: 'Physical Gold', value: 2493 },
  { month: 'Mar/26', asset: 'Global Gov Bond', value: 1666 },
  { month: 'Mar/26', asset: 'Core EUR Corp Bond', value: 1679 },
  { month: 'Mar/26', asset: 'MSCI World Value', value: 2387 },
  { month: 'Mar/26', asset: 'MSCI EM', value: 2033 },
  { month: 'Mar/26', asset: 'Defence Tech', value: 439.71 },
];

const pacSeed = [
  { month: 'Apr/26', asset: 'Core MSCI World', mode: 'Auto', amount: 640 },
  { month: 'Apr/26', asset: 'Physical Gold', mode: 'Auto', amount: 220 },
  { month: 'Apr/26', asset: 'Global Gov Bond', mode: 'Auto', amount: 52 },
  { month: 'Apr/26', asset: 'Core EUR Corp Bond', mode: 'Auto', amount: 54 },
  { month: 'Apr/26', asset: 'MSCI World Value', mode: 'Auto', amount: 180 },
  { month: 'Apr/26', asset: 'MSCI EM', mode: 'Auto', amount: 400 },
];

const manualSeed = [
  { month: 'Oct/25', asset: 'Core MSCI World', amount: 690.4 },
  { month: 'Oct/25', asset: 'AI & Big Data', amount: 101 },
  { month: 'Oct/25', asset: 'Physical Gold', amount: 70 },
  { month: 'Oct/25', asset: 'Global Gov Bond', amount: 52 },
  { month: 'Oct/25', asset: 'Core EUR Corp Bond', amount: 54 },
  { month: 'Oct/25', asset: 'MSCI World Value', amount: 196.99 },
  { month: 'Oct/25', asset: 'MSCI EM', amount: 44 },
  { month: 'Nov/25', asset: 'Core MSCI World', amount: 486 },
  { month: 'Nov/25', asset: 'Physical Gold', amount: 70 },
  { month: 'Nov/25', asset: 'Global Gov Bond', amount: 52 },
  { month: 'Nov/25', asset: 'Core EUR Corp Bond', amount: 54 },
  { month: 'Nov/25', asset: 'MSCI World Value', amount: 96 },
  { month: 'Nov/25', asset: 'MSCI EM', amount: 44 },
  { month: 'Dec/25', asset: 'Core MSCI World', amount: 486 },
  { month: 'Dec/25', asset: 'Physical Gold', amount: 70 },
  { month: 'Dec/25', asset: 'Global Gov Bond', amount: 52 },
  { month: 'Dec/25', asset: 'Core EUR Corp Bond', amount: 54 },
  { month: 'Dec/25', asset: 'MSCI World Value', amount: 96 },
  { month: 'Dec/25', asset: 'MSCI EM', amount: 44 },
  { month: 'Jan/26', asset: 'Core MSCI World', amount: 486 },
  { month: 'Jan/26', asset: 'Physical Gold', amount: 70 },
  { month: 'Jan/26', asset: 'Global Gov Bond', amount: 52 },
  { month: 'Jan/26', asset: 'Core EUR Corp Bond', amount: 54 },
  { month: 'Jan/26', asset: 'MSCI World Value', amount: 96 },
  { month: 'Jan/26', asset: 'MSCI EM', amount: 44 },
  { month: 'Feb/26', asset: 'Core MSCI World', amount: 486 },
  { month: 'Feb/26', asset: 'Physical Gold', amount: 70 },
  { month: 'Feb/26', asset: 'Global Gov Bond', amount: 52 },
  { month: 'Feb/26', asset: 'Core EUR Corp Bond', amount: 54 },
  { month: 'Feb/26', asset: 'MSCI World Value', amount: 96 },
  { month: 'Feb/26', asset: 'MSCI EM', amount: 44 },
  { month: 'Mar/26', asset: 'Core MSCI World', amount: 1539.76 },
  { month: 'Mar/26', asset: 'Physical Gold', amount: 220.99 },
  { month: 'Mar/26', asset: 'Global Gov Bond', amount: 52 },
  { month: 'Mar/26', asset: 'Core EUR Corp Bond', amount: 54 },
  { month: 'Mar/26', asset: 'MSCI World Value', amount: 497 },
  { month: 'Mar/26', asset: 'MSCI EM', amount: 645.99 },
];

const months = ['Oct/25', 'Nov/25', 'Dec/25', 'Jan/26', 'Feb/26', 'Mar/26', 'Apr/26'];
const palette = ['#60a5fa', '#2563eb', '#f59e0b', '#ef4444', '#34d399', '#14b8a6', '#facc15', '#f97316'];

function eur(v) {
  return new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR', maximumFractionDigits: 2 }).format(v || 0);
}

function pct(v) {
  if (v === null || v === undefined || Number.isNaN(v)) return '-';
  return `${v.toFixed(1)}%`;
}

function monthSortValue(m) {
  const [mm, yy] = m.split('/');
  const map = { Jan: 1, Feb: 2, Mar: 3, Apr: 4, May: 5, Jun: 6, Jul: 7, Aug: 8, Sep: 9, Oct: 10, Nov: 11, Dec: 12 };
  return (2000 + Number(yy)) * 100 + map[mm];
}

export default function PortfolioDashboardPrototype() {
  const [monthEnd, setMonthEnd] = useState(monthEndSeed);
  const [pacRows, setPacRows] = useState(pacSeed);
  const [manualRows, setManualRows] = useState(manualSeed);
  const [selectedMonth, setSelectedMonth] = useState('Mar/26');
  const [draftMonth, setDraftMonth] = useState('Apr/26');
  const [monthEndDraft, setMonthEndDraft] = useState(() => Object.fromEntries(assetsMaster.map(a => [a.name, ''])));
  const [manualForm, setManualForm] = useState({ month: 'Apr/26', asset: 'Core MSCI World', amount: '' });

  const monthEndMap = useMemo(() => {
    const map = new Map();
    monthEnd.forEach(r => map.set(`${r.month}__${r.asset}`, r.value));
    return map;
  }, [monthEnd]);

  const manualMap = useMemo(() => {
    const acc = new Map();
    manualRows.forEach(r => {
      const k = `${r.month}__${r.asset}`;
      acc.set(k, (acc.get(k) || 0) + Number(r.amount || 0));
    });
    return acc;
  }, [manualRows]);

  const pacMap = useMemo(() => {
    const acc = new Map();
    pacRows.forEach(r => {
      const k = `${r.month}__${r.asset}`;
      const value = r.mode === 'No' ? 0 : Number(r.amount || 0);
      acc.set(k, value);
    });
    return acc;
  }, [pacRows]);

  const etfAssets = assetsMaster.filter(a => a.category === 'ETF');

  const selectedMonthRows = useMemo(() => {
    return assetsMaster.map(asset => {
      const idx = months.indexOf(selectedMonth);
      const prevMonth = idx > 0 ? months[idx - 1] : null;
      const endValue = monthEndMap.get(`${selectedMonth}__${asset.name}`) || 0;
      const prevEnd = prevMonth ? (monthEndMap.get(`${prevMonth}__${asset.name}`) || 0) : 0;
      const flowPAC = pacMap.get(`${selectedMonth}__${asset.name}`) || 0;
      const flowManual = manualMap.get(`${selectedMonth}__${asset.name}`) || 0;
      const totalFlow = flowPAC + flowManual;
      const pnl = endValue && prevEnd ? endValue - prevEnd - totalFlow : null;
      const perfPct = pnl !== null && prevEnd > 0 ? (pnl / (prevEnd + totalFlow / 2)) * 100 : null;
      return { ...asset, endValue, prevEnd, flowPAC, flowManual, totalFlow, pnl, perfPct };
    });
  }, [selectedMonth, monthEndMap, pacMap, manualMap]);

  const kpis = useMemo(() => {
    const total = selectedMonthRows.reduce((s, r) => s + r.endValue, 0);
    const savings = selectedMonthRows.find(r => r.name === 'Savings')?.endValue || 0;
    const etf = total - savings;
    const flow = selectedMonthRows.reduce((s, r) => s + r.totalFlow, 0);
    const pnl = selectedMonthRows.filter(r => r.category === 'ETF' && r.pnl !== null).reduce((s, r) => s + r.pnl, 0);
    return { total, savings, etf, flow, pnl };
  }, [selectedMonthRows]);

  const pieData = useMemo(() => {
    return etfAssets
      .map(a => {
        const row = selectedMonthRows.find(r => r.name === a.name);
        return { name: a.name, value: row?.endValue || 0 };
      })
      .filter(r => r.value > 0);
  }, [selectedMonthRows]);

  const performanceBars = useMemo(() => {
    return selectedMonthRows
      .filter(r => r.category === 'ETF' && r.perfPct !== null)
      .map(r => ({ asset: r.name, perfPct: Number(r.perfPct.toFixed(1)) }));
  }, [selectedMonthRows]);

  const trendData = useMemo(() => {
    return months.slice(0, months.indexOf(selectedMonth) + 1).map(month => {
      const rows = assetsMaster.map(asset => {
        const val = monthEndMap.get(`${month}__${asset.name}`) || 0;
        return { ...asset, value: val };
      });
      const total = rows.reduce((s, r) => s + r.value, 0);
      const savings = rows.find(r => r.name === 'Savings')?.value || 0;
      const etf = total - savings;
      return { month, total, savings, etf };
    });
  }, [selectedMonth, monthEndMap]);

  const pacPreview = useMemo(() => {
    return etfAssets.filter(a => a.pac > 0).map(a => {
      const existing = pacRows.find(r => r.month === draftMonth && r.asset === a.name);
      return {
        asset: a.name,
        defaultPAC: a.pac,
        mode: existing?.mode || 'Auto',
        amount: existing?.amount ?? a.pac,
      };
    });
  }, [draftMonth, pacRows]);

  function saveMonthEnd() {
    const updates = Object.entries(monthEndDraft)
      .filter(([, value]) => value !== '' && !Number.isNaN(Number(value)))
      .map(([asset, value]) => ({ month: draftMonth, asset, value: Number(value) }));

    if (!updates.length) return;

    setMonthEnd(prev => {
      const filtered = prev.filter(r => !(r.month === draftMonth && updates.some(u => u.asset === r.asset)));
      return [...filtered, ...updates].sort((a, b) => monthSortValue(a.month) - monthSortValue(b.month));
    });
    setSelectedMonth(draftMonth);
    setMonthEndDraft(Object.fromEntries(assetsMaster.map(a => [a.name, ''])));
  }

  function updatePac(month, asset, patch) {
    setPacRows(prev => {
      const exists = prev.find(r => r.month === month && r.asset === asset);
      if (!exists) {
        const base = assetsMaster.find(a => a.name === asset)?.pac || 0;
        return [...prev, { month, asset, mode: 'Auto', amount: base, ...patch }];
      }
      return prev.map(r => (r.month === month && r.asset === asset ? { ...r, ...patch } : r));
    });
  }

  function addManualTransaction() {
    if (!manualForm.month || !manualForm.asset || !manualForm.amount) return;
    setManualRows(prev => [...prev, { month: manualForm.month, asset: manualForm.asset, amount: Number(manualForm.amount) }]);
    setManualForm({ month: draftMonth, asset: 'Core MSCI World', amount: '' });
    setSelectedMonth(manualForm.month);
  }

  const etfSharePct = kpis.total > 0 ? (kpis.etf / kpis.total) * 100 : 0;
  const savingsSharePct = kpis.total > 0 ? (kpis.savings / kpis.total) * 100 : 0;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-6">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold tracking-tight">Portfolio Dashboard</h1>
            <p className="text-slate-400 mt-1">Prototype V2 - month end update, PAC confirmation, manual transactions</p>
          </div>
          <div className="flex gap-3 items-center">
            <Badge className="bg-emerald-500/20 text-emerald-300 border border-emerald-400/20">Selected month: {selectedMonth}</Badge>
            <Select value={selectedMonth} onValueChange={setSelectedMonth}>
              <SelectTrigger className="w-[140px] bg-slate-900 border-slate-800">
                <SelectValue placeholder="Month" />
              </SelectTrigger>
              <SelectContent>
                {months.map(m => <SelectItem key={m} value={m}>{m}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-4">
          {[
            { label: 'Portfolio Total', value: eur(kpis.total), icon: Wallet },
            { label: 'ETF Total', value: eur(kpis.etf), icon: TrendingUp },
            { label: 'Savings', value: eur(kpis.savings), icon: PiggyBank },
            { label: 'Monthly Flow', value: eur(kpis.flow), icon: Euro },
            { label: 'ETF PnL', value: eur(kpis.pnl), icon: Activity, negative: kpis.pnl < 0 },
          ].map((kpi, i) => {
            const Icon = kpi.icon;
            return (
              <motion.div key={kpi.label} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.03 }}>
                <Card className="bg-slate-900/80 border-slate-800 rounded-3xl shadow-xl">
                  <CardContent className="p-5">
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="text-sm text-slate-400">{kpi.label}</p>
                        <p className={`text-2xl font-bold mt-2 ${kpi.negative ? 'text-red-400' : 'text-white'}`}>{kpi.value}</p>
                      </div>
                      <div className="h-10 w-10 rounded-2xl bg-slate-800 flex items-center justify-center">
                        <Icon className="w-5 h-5 text-slate-300" />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          <Card className="xl:col-span-2 bg-slate-900/80 border-slate-800 rounded-3xl">
            <CardHeader>
              <CardTitle className="text-xl">Portfolio trend</CardTitle>
            </CardHeader>
            <CardContent className="h-[340px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trendData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="month" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" tickFormatter={v => eur(v).replace(',00', '')} />
                  <Tooltip formatter={(v) => eur(Number(v))} contentStyle={{ background: '#020617', border: '1px solid #1e293b', borderRadius: 16 }} />
                  <Legend />
                  <Line type="monotone" dataKey="total" stroke="#e2e8f0" strokeWidth={3} dot={false} name="Total" />
                  <Line type="monotone" dataKey="etf" stroke="#60a5fa" strokeWidth={3} dot={false} name="ETF" />
                  <Line type="monotone" dataKey="savings" stroke="#22c55e" strokeWidth={3} dot={false} name="Savings" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/80 border-slate-800 rounded-3xl">
            <CardHeader>
              <CardTitle className="text-xl">Split</CardTitle>
            </CardHeader>
            <CardContent className="space-y-5">
              <div>
                <div className="flex justify-between text-sm mb-2"><span className="text-slate-400">ETF</span><span>{etfSharePct.toFixed(1)}%</span></div>
                <Progress value={etfSharePct} className="h-3" />
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2"><span className="text-slate-400">Savings</span><span>{savingsSharePct.toFixed(1)}%</span></div>
                <Progress value={savingsSharePct} className="h-3" />
              </div>
              <div className="h-[220px]">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={55} outerRadius={90} paddingAngle={2}>
                      {pieData.map((_, index) => <Cell key={index} fill={palette[index % palette.length]} />)}
                    </Pie>
                    <Tooltip formatter={(v) => eur(Number(v))} contentStyle={{ background: '#020617', border: '1px solid #1e293b', borderRadius: 16 }} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          <Card className="bg-slate-900/80 border-slate-800 rounded-3xl">
            <CardHeader>
              <CardTitle className="text-xl">ETF monthly performance</CardTitle>
            </CardHeader>
            <CardContent className="h-[340px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={performanceBars}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="asset" angle={-20} textAnchor="end" interval={0} height={80} stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" tickFormatter={(v) => `${v}%`} />
                  <Tooltip formatter={(v) => `${Number(v).toFixed(1)}%`} contentStyle={{ background: '#020617', border: '1px solid #1e293b', borderRadius: 16 }} />
                  <Bar dataKey="perfPct" radius={[10, 10, 0, 0]}>
                    {performanceBars.map((r, idx) => <Cell key={idx} fill={r.perfPct >= 0 ? '#60a5fa' : '#f87171'} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/80 border-slate-800 rounded-3xl">
            <CardHeader>
              <CardTitle className="text-xl">Current month detail</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 max-h-[340px] overflow-auto pr-2">
              {selectedMonthRows.filter(r => r.category === 'ETF').map((row) => (
                <div key={row.name} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="font-semibold">{row.name}</p>
                      <p className="text-xs text-slate-400">End {eur(row.endValue)} - Flow {eur(row.totalFlow)}</p>
                    </div>
                    <Badge className={`${(row.perfPct || 0) >= 0 ? 'bg-emerald-500/20 text-emerald-300' : 'bg-red-500/20 text-red-300'} border-0`}>{pct(row.perfPct)}</Badge>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="month-end" className="w-full">
          <TabsList className="grid grid-cols-3 w-full bg-slate-900 border border-slate-800 rounded-2xl">
            <TabsTrigger value="month-end">Update Month End</TabsTrigger>
            <TabsTrigger value="pac">Confirm PAC</TabsTrigger>
            <TabsTrigger value="manual">Manual Transaction</TabsTrigger>
          </TabsList>

          <TabsContent value="month-end" className="mt-6">
            <Card className="bg-slate-900/80 border-slate-800 rounded-3xl">
              <CardHeader className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                  <CardTitle className="text-xl">Insert month end values</CardTitle>
                  <p className="text-sm text-slate-400 mt-1">Only final month values. Dashboard calculates flow and performance.</p>
                </div>
                <Select value={draftMonth} onValueChange={setDraftMonth}>
                  <SelectTrigger className="w-[140px] bg-slate-950 border-slate-800"><SelectValue /></SelectTrigger>
                  <SelectContent>{months.map(m => <SelectItem key={m} value={m}>{m}</SelectItem>)}</SelectContent>
                </Select>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                  {assetsMaster.map(asset => (
                    <div key={asset.name} className="rounded-2xl border border-slate-800 p-4 bg-slate-950/60">
                      <p className="font-medium mb-2">{asset.name}</p>
                      <Input
                        type="number"
                        placeholder="Month end value"
                        value={monthEndDraft[asset.name]}
                        onChange={(e) => setMonthEndDraft(prev => ({ ...prev, [asset.name]: e.target.value }))}
                        className="bg-slate-900 border-slate-800"
                      />
                    </div>
                  ))}
                </div>
                <div className="mt-5 flex justify-end">
                  <Button onClick={saveMonthEnd} className="rounded-2xl bg-white text-slate-900 hover:bg-slate-200">
                    <PlusCircle className="w-4 h-4 mr-2" /> Save month end
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="pac" className="mt-6">
            <Card className="bg-slate-900/80 border-slate-800 rounded-3xl">
              <CardHeader className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                  <CardTitle className="text-xl">Confirm monthly PAC</CardTitle>
                  <p className="text-sm text-slate-400 mt-1">Auto keeps the default PAC from Assets. No skips the month. Edited overrides the amount.</p>
                </div>
                <Select value={draftMonth} onValueChange={setDraftMonth}>
                  <SelectTrigger className="w-[140px] bg-slate-950 border-slate-800"><SelectValue /></SelectTrigger>
                  <SelectContent>{months.map(m => <SelectItem key={m} value={m}>{m}</SelectItem>)}</SelectContent>
                </Select>
              </CardHeader>
              <CardContent className="space-y-4">
                {pacPreview.map((row) => (
                  <div key={row.asset} className="grid grid-cols-1 md:grid-cols-[1.4fr_0.8fr_0.8fr] gap-3 items-center rounded-2xl border border-slate-800 p-4 bg-slate-950/60">
                    <div>
                      <p className="font-semibold">{row.asset}</p>
                      <p className="text-xs text-slate-400">Default PAC {eur(row.defaultPAC)}</p>
                    </div>
                    <Select value={row.mode} onValueChange={(v) => updatePac(draftMonth, row.asset, { mode: v })}>
                      <SelectTrigger className="bg-slate-900 border-slate-800"><SelectValue /></SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Auto">Auto</SelectItem>
                        <SelectItem value="Edited">Edited</SelectItem>
                        <SelectItem value="No">No</SelectItem>
                      </SelectContent>
                    </Select>
                    <Input
                      type="number"
                      value={row.amount}
                      disabled={row.mode === 'No'}
                      onChange={(e) => updatePac(draftMonth, row.asset, { amount: Number(e.target.value || 0), mode: row.mode === 'Auto' ? 'Edited' : row.mode })}
                      className="bg-slate-900 border-slate-800"
                    />
                  </div>
                ))}
                <div className="flex items-center gap-2 text-sm text-slate-400 pt-2">
                  <CheckCircle2 className="w-4 h-4" /> Changes are reflected instantly in the dashboard preview.
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="manual" className="mt-6">
            <Card className="bg-slate-900/80 border-slate-800 rounded-3xl">
              <CardHeader>
                <CardTitle className="text-xl">Add manual transaction</CardTitle>
                <p className="text-sm text-slate-400 mt-1">Use this only for extras outside PAC.</p>
              </CardHeader>
              <CardContent className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Select value={manualForm.month} onValueChange={(v) => setManualForm(prev => ({ ...prev, month: v }))}>
                  <SelectTrigger className="bg-slate-950 border-slate-800"><SelectValue /></SelectTrigger>
                  <SelectContent>{months.map(m => <SelectItem key={m} value={m}>{m}</SelectItem>)}</SelectContent>
                </Select>
                <Select value={manualForm.asset} onValueChange={(v) => setManualForm(prev => ({ ...prev, asset: v }))}>
                  <SelectTrigger className="bg-slate-950 border-slate-800"><SelectValue /></SelectTrigger>
                  <SelectContent>{etfAssets.map(a => <SelectItem key={a.name} value={a.name}>{a.name}</SelectItem>)}</SelectContent>
                </Select>
                <Input type="number" placeholder="Amount" value={manualForm.amount} onChange={(e) => setManualForm(prev => ({ ...prev, amount: e.target.value }))} className="bg-slate-950 border-slate-800" />
                <Button onClick={addManualTransaction} className="rounded-2xl bg-white text-slate-900 hover:bg-slate-200">
                  <PencilLine className="w-4 h-4 mr-2" /> Add transaction
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        <Card className="bg-slate-900/80 border-slate-800 rounded-3xl">
          <CardHeader>
            <CardTitle className="text-xl">How this should work in the real app</CardTitle>
          </CardHeader>
          <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm text-slate-300">
            <div className="space-y-2">
              <p className="font-semibold text-white">1. End of month</p>
              <p>Open the app, select the month, type savings and ETF final values, click save.</p>
            </div>
            <div className="space-y-2">
              <p className="font-semibold text-white">2. PAC review</p>
              <p>Leave Auto if the monthly PAC is correct, change to No if skipped, Edited if you changed the amount.</p>
            </div>
            <div className="space-y-2">
              <p className="font-semibold text-white">3. Manual extras</p>
              <p>Add only extra buys outside PAC. Dashboard separates flow from market performance.</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
