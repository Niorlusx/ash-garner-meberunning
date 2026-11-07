"""MBR Daily Ops Agent - deterministic daily catalog and release pipeline.

Ash Garner / MBR Records / 3630. Runs unattended on a schedule:
builds the SoundCloud upload queue, YouTube queue, store-delivery request
list, and the Control Room daily checks, then compiles an ops report.
"""
from datetime import datetime, timezone

from pydantic import BaseModel, Field

import mistralai.workflows as workflows

SOUNDCLOUD_UPLOADS = [
    "Day 2 Way",
    "Unloved",
    "Strip Slut (Explicit)",
    "Sun in the West",
    "Soul On Fire (Remix)",
    "Ripping It Up",
]

YOUTUBE_QUEUE = [
    "Soul On Fire (full 16:9 MV)",
    "Loyalty (full master)",
    "Watch Table (uncut master)",
    "New Souls (uncut master)",
    "Thirty-Six Thirty (Remastered)",
]

STORE_DELIVERY_REQUESTS = [
    "Meberunning",
    "Soul On Fire",
    "She Talkin With It (Explicit)",
    "Watch Table",
    "Loyalty",
    "Up But Grounded",
    "Dollar Signs",
    "Mental Life",
    "New Souls",
    "Hit Down Hard",
    "Harder End",
    "Pulse in My Throat",
    "Thirty-Six Thirty (Remastered)",
]

PRIVATE_LANE = [
    "I'm Sorry Shakeah",
    "Earn Back Trust",
    "Happy Birthday Shakeah",
]

DAILY_CHECKS = [
    "Official folder count (Drive Officials)",
    "Imagine credit status",
    "music-hub /health after deploy",
    "Vercel landing production domain",
    "No engagement-push jobs",
    "Mark completed uploads LIVE in the Unified Master Sync sheet",
    "Request SoundCloud monetization for new uploads",
    "Private Lane stays private - no store delivery",
]


class DailyOpsInput(BaseModel):
    date: str = ""
    include_private_lane: bool = False


class DailyOpsReport(BaseModel):
    date: str
    soundcloud_uploads_needed: list[str] = Field(default_factory=list)
    youtube_queue: list[str] = Field(default_factory=list)
    store_delivery_requests: list[str] = Field(default_factory=list)
    daily_checks: list[str] = Field(default_factory=list)
    private_lane_guard: list[str] = Field(default_factory=list)
    summary: str = ""


@workflows.activity()
async def build_queues(include_private_lane: bool) -> dict:
    """Return the current upload and delivery queues for the catalog."""
    queues = {
        "soundcloud": list(SOUNDCLOUD_UPLOADS),
        "youtube": list(YOUTUBE_QUEUE),
        "store_delivery": list(STORE_DELIVERY_REQUESTS),
        "private_lane": list(PRIVATE_LANE) if include_private_lane else [],
    }
    return queues


@workflows.activity()
async def build_daily_checks() -> list[str]:
    """Return the Control Room daily checklist."""
    return list(DAILY_CHECKS)


@workflows.activity()
async def compile_report(date: str, queues: dict, checks: list[str]) -> DailyOpsReport:
    """Compile the daily ops report from queues and checks."""
    sc = len(queues["soundcloud"])
    yt = len(queues["youtube"])
    sd = len(queues["store_delivery"])
    summary = (
        f"MBR Records daily ops {date}: {sc} SoundCloud uploads pending, "
        f"{yt} YouTube items queued, {sd} store delivery requests outstanding. "
        "Private Lane guard active."
    )
    return DailyOpsReport(
        date=date,
        soundcloud_uploads_needed=queues["soundcloud"],
        youtube_queue=queues["youtube"],
        store_delivery_requests=queues["store_delivery"],
        daily_checks=checks,
        private_lane_guard=queues["private_lane"],
        summary=summary,
    )


@workflows.workflow.define(
    name="mbr-daily-ops",
    workflow_display_name="MBR Daily Ops Agent",
    workflow_description=(
        "Daily MBR Records ops pipeline for Ash Garner: SoundCloud upload queue, "
        "YouTube queue, store delivery requests and Control Room daily checks."
    ),
)
class MbrDailyOpsWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, input: DailyOpsInput) -> DailyOpsReport:
        date = input.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        queues = await build_queues(input.include_private_lane)
        checks = await build_daily_checks()
        report = await compile_report(date, queues, checks)
        return report
