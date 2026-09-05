interface MetricStripProps {
  precision: number;
  recall: number;
  falsePositiveCostInr: number;
  recoveryRate: number;
}

export function MetricStrip({ precision, recall, falsePositiveCostInr, recoveryRate }: MetricStripProps) {
  const metrics = [
    { label: "Precision", value: `${Math.round(precision * 100)}%` },
    { label: "Recall", value: `${Math.round(recall * 100)}%` },
    { label: "False-positive cost", value: `₹${falsePositiveCostInr.toLocaleString("en-IN")}` },
    { label: "Revenue recovery rate", value: `${Math.round(recoveryRate * 100)}%` },
  ];

  return (
    <div className="grid grid-cols-4 divide-x divide-paper/10 border-b border-paper/10">
      {metrics.map((m) => (
        <div key={m.label} className="px-6 py-4">
          <p className="text-xs text-slate uppercase tracking-wide mb-1">{m.label}</p>
          <p className="font-data text-xl text-paper tabular-nums">{m.value}</p>
        </div>
      ))}
    </div>
  );
}
