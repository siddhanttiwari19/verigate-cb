"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ShieldCheck, WifiOff } from "lucide-react";
import { mockDisputes, mockEvalReport } from "@/lib/mockData";
import { DisputeRecord } from "@/types/dispute";
import { DisputeRow } from "@/components/DisputeRow";
import { CaseDetail } from "@/components/CaseDetail";
import { MetricStrip } from "@/components/MetricStrip";

export default function ConsolePage() {
  const [disputes, setDisputes] = useState<DisputeRecord[]>(mockDisputes);
  const [evalReport, setEvalReport] = useState(mockEvalReport);
  const [activeKey, setActiveKey] = useState<string>(
    `${mockDisputes[0].dispute_id}::${mockDisputes[0].timestamp}`
  );
  const [isLive, setIsLive] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function loadRealData() {
      try {
        const [historyRes, evalRes] = await Promise.all([
          fetch("/api/disputes-history"),
          fetch("/api/eval-report"),
        ]);

        if (!historyRes.ok || !evalRes.ok) return;

        const history: DisputeRecord[] = await historyRes.json();
        const evalData = await evalRes.json();

        if (cancelled || history.length === 0) return;

        setDisputes(history);
        setEvalReport(evalData);
        setActiveKey(`${history[0].dispute_id}::${history[0].timestamp}`);
        setIsLive(true);
      } catch {
        // Backend not running — mock data stays as the fallback, no error shown.
      }
    }

    loadRealData();
    return () => {
      cancelled = true;
    };
  }, []);

  const activeDispute =
    disputes.find((d) => `${d.dispute_id}::${d.timestamp}` === activeKey) ?? null;

  return (
    <div className="flex flex-col h-screen bg-ink">
      <header className="flex items-center justify-between px-6 py-3.5 border-b border-paper/10">
        <Link href="/" className="flex items-center gap-2">
          <ShieldCheck size={18} className="text-verified" strokeWidth={2.25} />
          <span className="font-display italic text-lg text-paper">verigate</span>
        </Link>
        <span className="flex items-center gap-1.5 text-xs text-slate">
          {isLive ? (
            <>Risk ops console · live backend data</>
          ) : (
            <>
              <WifiOff size={12} />
              Risk ops console · demo data (backend not connected)
            </>
          )}
        </span>
      </header>

      <MetricStrip
        precision={evalReport.precision}
        recall={evalReport.recall}
        falsePositiveCostInr={evalReport.false_positive_cost_inr}
        recoveryRate={evalReport.recovery_rate}
      />

      <div className="flex flex-1 min-h-0">
        <aside className="w-[320px] shrink-0 border-r border-paper/10 overflow-y-auto">
          <div className="px-4 py-3 border-b border-paper/10">
            <p className="text-xs text-slate uppercase tracking-wide">
              Dispute queue · {disputes.length}
            </p>
          </div>
          {disputes.map((dispute, i) => {
            const rowKey = `${dispute.dispute_id}::${dispute.timestamp}`;
            return (
              <DisputeRow
                key={rowKey}
                dispute={dispute}
                isActive={rowKey === activeKey}
                onSelect={() => setActiveKey(rowKey)}
                index={i}
              />
            );
          })}
        </aside>

        <CaseDetail dispute={activeDispute} />
      </div>
    </div>
  );
}