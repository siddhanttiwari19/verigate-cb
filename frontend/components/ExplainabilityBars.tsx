import { EvidenceFactor } from "@/types/dispute";

export function ExplainabilityBars({ factors }: { factors: EvidenceFactor[] }) {
  const maxAbs = Math.max(...factors.map((f) => Math.abs(f.contribution)), 0.01);

  return (
    <div className="space-y-2.5">
      {factors.map((factor) => {
        const isPositive = factor.direction === "supports winning";
        const widthPct = (Math.abs(factor.contribution) / maxAbs) * 100;

        return (
          <div key={factor.factor} className="grid grid-cols-[1fr_auto] gap-3 items-center">
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm text-paper/90">{factor.factor}</span>
                <span className="font-data text-xs text-slate tabular-nums">
                  {factor.contribution > 0 ? "+" : ""}
                  {factor.contribution.toFixed(3)}
                </span>
              </div>
              <div className="h-1.5 rounded-full bg-ink-raised overflow-hidden">
                <div
                  className={`h-full rounded-full ${isPositive ? "bg-verified" : "bg-rejected"}`}
                  style={{ width: `${widthPct}%` }}
                />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
