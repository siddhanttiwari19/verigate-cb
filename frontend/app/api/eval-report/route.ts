import { NextResponse } from "next/server";

export async function GET() {
  const backendUrl = process.env.BACKEND_URL ?? "http://localhost:8000";
  const apiKey = process.env.BACKEND_API_KEY;

  if (!apiKey) {
    return NextResponse.json(
      { error: "BACKEND_API_KEY is not set in .env.local" },
      { status: 500 }
    );
  }

  try {
    const res = await fetch(`${backendUrl}/model/eval-report`, {
      headers: { "X-API-Key": apiKey },
      cache: "no-store",
    });

    if (!res.ok) {
      return NextResponse.json(
        { error: `Backend returned ${res.status}` },
        { status: res.status }
      );
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json(
      { error: "Could not reach backend. Is uvicorn running on port 8000?" },
      { status: 502 }
    );
  }
}
