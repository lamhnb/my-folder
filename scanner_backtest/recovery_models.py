from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DowntimeType(str, Enum):
    SHORT_GAP = "SHORT_GAP"
    MEDIUM_GAP = "MEDIUM_GAP"
    LONG_GAP = "LONG_GAP"
    FULL_REBUILD = "FULL_REBUILD"


class DetectionMode(str, Enum):
    LIVE = "LIVE"
    RECOVERED = "RECOVERED"
    BACKFILLED = "BACKFILLED"
    REBUILT = "REBUILT"


class ReconstructionStatus(str, Enum):
    FULLY_RECONSTRUCTED = "FULLY_RECONSTRUCTED"
    PARTIALLY_RECONSTRUCTED = "PARTIALLY_RECONSTRUCTED"
    LIVE_ONLY = "LIVE_ONLY"
    UNKNOWN = "UNKNOWN"
    MISSING_DURING_DOWNTIME = "MISSING_DURING_DOWNTIME"
    EXPIRED = "EXPIRED"


class FreshnessStatus(str, Enum):
    FRESH = "FRESH"
    STALE = "STALE"
    EXPIRED = "EXPIRED"
    UNKNOWN = "UNKNOWN"


class DataConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ReadinessState(str, Enum):
    NOT_READY = "NOT_READY"
    HISTORICAL_READY = "HISTORICAL_READY"
    LIVE_WARMING = "LIVE_WARMING"
    PARTIALLY_READY = "PARTIALLY_READY"
    FULLY_READY = "FULLY_READY"


class RecoveryRunStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    RETRYING = "RETRYING"
    SUCCESS = "SUCCESS"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    FAILED = "FAILED"
    ABORTED = "ABORTED"


class CheckpointStatus(str, Enum):
    CREATING = "CREATING"
    VALID = "VALID"
    PARTIAL = "PARTIAL"
    CORRUPTED = "CORRUPTED"
    SUPERSEDED = "SUPERSEDED"


class MarketState(str, Enum):
    BASE_FORMATION = "BASE_FORMATION"
    SUPPLY_ABSORPTION = "SUPPLY_ABSORPTION"
    POSITIONING_BUILDUP = "POSITIONING_BUILDUP"
    COMPRESSION = "COMPRESSION"
    PRE_IGNITION = "PRE_IGNITION"
    IGNITION = "IGNITION"
    EXPANSION = "EXPANSION"
    DISTRIBUTION = "DISTRIBUTION"
    FAILED_BREAKOUT = "FAILED_BREAKOUT"
    INVALIDATED = "INVALIDATED"


class MarketOverlay(str, Enum):
    WEEKLY_ACCEPTANCE = "WEEKLY_ACCEPTANCE"
    PARABOLIC_RISK = "PARABOLIC_RISK"
    SHORT_SQUEEZE_FUEL = "SHORT_SQUEEZE_FUEL"
    LONG_SQUEEZE_RISK = "LONG_SQUEEZE_RISK"
    DATA_DEGRADED = "DATA_DEGRADED"


class RecoveredSetupClass(str, Enum):
    ACTIVE_RECOVERED_SETUP = "ACTIVE_RECOVERED_SETUP"
    RECOVERED_IGNITION = "RECOVERED_IGNITION"
    MISSED_MOVE = "MISSED_MOVE"
    RECOVERED_FAILED_BREAKOUT = "RECOVERED_FAILED_BREAKOUT"
    EXPIRED_SETUP = "EXPIRED_SETUP"
    INVALIDATED_SETUP = "INVALIDATED_SETUP"
    RECOVERED_DISTRIBUTION = "RECOVERED_DISTRIBUTION"
    NO_ACTION = "NO_ACTION"


class EntryQuality(str, Enum):
    ENTRY_EARLY = "ENTRY_EARLY"
    ENTRY_ACCEPTABLE = "ENTRY_ACCEPTABLE"
    RETEST_ONLY = "RETEST_ONLY"
    LATE_ENTRY = "LATE_ENTRY"
    DO_NOT_CHASE = "DO_NOT_CHASE"
    UNKNOWN = "UNKNOWN"


@dataclass(slots=True)
class Checkpoint:
    checkpoint_id: str
    created_at_ms: int
    scanner_version: str
    config_version: str
    schema_version: int
    last_successful_scan_time_ms: int
    last_complete_market_timestamp_ms: int
    last_complete_oi_timestamp_ms: int
    last_complete_funding_timestamp_ms: int
    last_complete_event_timestamp_ms: int
    symbol_count: int
    state_snapshot_hash: str
    feature_snapshot_hash: str
    data_source_status: dict[str, Any]
    checkpoint_status: CheckpointStatus


@dataclass(slots=True)
class DowntimeGap:
    start_ms: int
    end_ms: int
    duration_ms: int
    gap_type: DowntimeType
    checkpoint_id: str | None = None


@dataclass(slots=True)
class CoverageSnapshot:
    symbol: str
    historical_coverage: float = 0.0
    oi_coverage: float = 0.0
    funding_coverage: float = 0.0
    trade_flow_coverage: float = 0.0
    microstructure_coverage: float = 0.0
    event_data_coverage: float = 0.0
    reconstruction_status: ReconstructionStatus = ReconstructionStatus.UNKNOWN
    data_confidence: float = 0.0
    confidence_level: DataConfidenceLevel = DataConfidenceLevel.LOW
    missing_feature_groups: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class LifecycleSnapshot:
    symbol: str
    state: MarketState = MarketState.BASE_FORMATION
    overlays: set[MarketOverlay] = field(default_factory=set)
    state_started_at_ms: int = 0
    last_confirmed_at_ms: int = 0
    expires_at_ms: int = 0
    base_price: float | None = None
    breakout_price: float | None = None
    ignition_time_ms: int | None = None
    invalidation_price: float | None = None
    persistence_count: int = 0
    evidence_score: float = 0.0
    data_confidence: float = 0.0
    setup_id: str | None = None
    last_event_time_ms: int = 0


@dataclass(slots=True)
class StateTransition:
    symbol: str
    from_state: MarketState
    to_state: MarketState
    event_time_ms: int
    detected_time_ms: int
    detection_mode: DetectionMode
    reason: str
    evidence: dict[str, Any]
    setup_id: str | None = None
    recovery_run_id: str | None = None


@dataclass(slots=True)
class StateEvidence:
    event_time_ms: int
    price: float
    atr: float
    base_price: float
    base_high: float
    base_low: float
    distance_from_base_atr: float
    distance_from_breakout_atr: float
    compression_score: float
    absorption_score: float
    failed_breakdown_score: float
    downside_exhaustion: float
    positioning_score: float
    ignition_score: float
    distribution_score: float
    funding_crowding: float
    short_squeeze_fuel: float
    long_squeeze_risk: float
    data_confidence: float
    breakout_price: float | None = None
    invalidation_price: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RecoveredSetup:
    symbol: str
    classification: RecoveredSetupClass
    current_state: MarketState
    event_time_ms: int
    detected_time_ms: int
    entry_quality: EntryQuality
    distance_from_base_atr: float | None
    data_confidence: float
    explanation: str
    setup_id: str | None = None


@dataclass(slots=True)
class RecoveryResult:
    recovery_run_id: str
    status: RecoveryRunStatus
    gap: DowntimeGap
    checkpoint_used: str | None
    symbols_processed: int
    symbols_failed: int
    coverage: dict[str, CoverageSnapshot]
    lifecycle: dict[str, LifecycleSnapshot]
    transitions: list[StateTransition]
    recovered_setups: list[RecoveredSetup]
    alerts_suppressed: int
