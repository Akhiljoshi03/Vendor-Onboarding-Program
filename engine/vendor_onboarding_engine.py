"""
Vendor Onboarding & SLA Automation Engine
-------------------------------------------
Automates the SOP, tracks SLAs per stage, runs the catalog QA gate,
and generates a stakeholder status report for the multi-vendor
onboarding pipeline described in SOP_vendor_onboarding.md and
RACI_matrix.md.
"""
import datetime
from enum import Enum
from typing import List, Dict, Optional
import random


# ==========================================
# 1. ENUMS & CONSTANTS (Mapping to RACI & SOP)
# ==========================================
class OnboardingStage(Enum):
    INITIATED = "Vendor Initiated"
    DATA_INGESTION = "Raw Data Ingestion"
    METADATA_ENRICHMENT = "Metadata Enrichment"
    QA_REVIEW = "Quality Assurance"
    LIVE = "Live on Storefront"


class Status(Enum):
    ON_TRACK = "On Track"
    AT_RISK = "At Risk"
    BLOCKED = "Blocked"


# SLA definitions from the SOP (in days)
SLA_THRESHOLDS = {
    OnboardingStage.INITIATED: 1,
    OnboardingStage.DATA_INGESTION: 3,
    OnboardingStage.METADATA_ENRICHMENT: 2,
    OnboardingStage.QA_REVIEW: 2,
}

# RACI accountability mapping
OWNERSHIP_MAP = {
    OnboardingStage.INITIATED: "Vendor Relations",
    OnboardingStage.DATA_INGESTION: "Data Ops Team",
    OnboardingStage.METADATA_ENRICHMENT: "AI Cataloging System",
    OnboardingStage.QA_REVIEW: "QA & Compliance",
    OnboardingStage.LIVE: "Storefront Ops",
}


# ==========================================
# 2. DATA MODELS
# ==========================================
class CatalogItem:
    def __init__(self, sku: str, title: str, has_images: bool, fabric_data: Optional[str] = None):
        self.sku = sku
        self.title = title
        self.has_images = has_images
        self.fabric_data = fabric_data
        self.is_valid = False
        self.rejection_reason = []

    def validate_against_sop(self) -> bool:
        """Enforces the SOP requirements for a valid catalog item."""
        self.rejection_reason = []
        if not self.has_images:
            self.rejection_reason.append("Missing high-res imagery")
        if not self.fabric_data:
            self.rejection_reason.append("Missing mandatory fabric composition")

        self.is_valid = len(self.rejection_reason) == 0
        return self.is_valid

    def to_dict(self):
        return {
            "sku": self.sku,
            "title": self.title,
            "is_valid": self.is_valid,
            "errors": self.rejection_reason,
        }


class Vendor:
    def __init__(self, vendor_id: str, name: str, sku_count: int):
        self.vendor_id = vendor_id
        self.name = name
        self.stage = OnboardingStage.INITIATED
        self.status = Status.ON_TRACK
        self.date_entered_current_stage = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 5))
        self.catalog_items: List[CatalogItem] = []
        self.blocker_notes: str = ""
        self._generate_mock_catalog(sku_count)

    def _generate_mock_catalog(self, count: int):
        for i in range(count):
            # Simulate real-world messy data where ~15% of items have issues
            has_img = random.random() > 0.15
            has_fabric = random.random() > 0.10
            self.catalog_items.append(
                CatalogItem(
                    sku=f"{self.vendor_id}-SKU-{i+1000}",
                    title=f"Sample Garment {i+1}",
                    has_images=has_img,
                    fabric_data="100% Cotton" if has_fabric else None,
                )
            )

    def days_in_current_stage(self) -> int:
        return (datetime.datetime.now() - self.date_entered_current_stage).days

    def current_owner(self) -> str:
        return OWNERSHIP_MAP.get(self.stage, "Unassigned")


# ==========================================
# 3. CORE AUTOMATION ENGINE (Program Management)
# ==========================================
class VendorOnboardingEngine:
    def __init__(self):
        self.vendors: Dict[str, Vendor] = {}
        self.blocker_log: List[dict] = []

    def add_vendor(self, vendor: Vendor):
        self.vendors[vendor.vendor_id] = vendor

    def evaluate_slas(self):
        """Scans all vendors and updates status based on SOP SLA thresholds."""
        for vendor in self.vendors.values():
            if vendor.stage == OnboardingStage.LIVE:
                continue

            days_active = vendor.days_in_current_stage()
            allowed_days = SLA_THRESHOLDS.get(vendor.stage, 99)
            if days_active > allowed_days + 2:
                vendor.status = Status.BLOCKED
                vendor.blocker_notes = f"SLA Breach: Stuck in {vendor.stage.value} for {days_active} days."
                self._log_blocker(vendor)
            elif days_active > allowed_days:
                vendor.status = Status.AT_RISK
            else:
                vendor.status = Status.ON_TRACK

    def run_catalog_qa_gate(self, vendor_id: str):
        """Automates the QA SOP by scanning catalog items for compliance."""
        vendor = self.vendors.get(vendor_id)
        if not vendor:
            return

        failed_items = 0
        for item in vendor.catalog_items:
            if not item.validate_against_sop():
                failed_items += 1

        error_rate = failed_items / len(vendor.catalog_items) if vendor.catalog_items else 0

        # SOP rule: if error rate > 5%, block the vendor and bounce back to Data Ops
        if error_rate > 0.05:
            vendor.status = Status.BLOCKED
            vendor.blocker_notes = f"QA Failed: {failed_items} items ({error_rate:.1%}) missing mandatory metadata."
            self._log_blocker(vendor)
        elif vendor.stage == OnboardingStage.QA_REVIEW and vendor.status != Status.BLOCKED:
            self.transition_vendor_stage(vendor_id, OnboardingStage.LIVE)

    def transition_vendor_stage(self, vendor_id: str, new_stage: OnboardingStage):
        vendor = self.vendors.get(vendor_id)
        if vendor and vendor.stage != new_stage:
            vendor.stage = new_stage
            vendor.date_entered_current_stage = datetime.datetime.now()
            vendor.status = Status.ON_TRACK
            vendor.blocker_notes = ""

    def _log_blocker(self, vendor: Vendor):
        self.blocker_log.append({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "vendor": vendor.name,
            "stage": vendor.stage.value,
            "owner": vendor.current_owner(),
            "issue": vendor.blocker_notes,
        })

    def generate_stakeholder_report(self) -> str:
        """Generates the automated stakeholder comms report."""
        self.evaluate_slas()

        live_count = sum(1 for v in self.vendors.values() if v.stage == OnboardingStage.LIVE)
        blocked_vendors = [v for v in self.vendors.values() if v.status == Status.BLOCKED]
        at_risk_vendors = [v for v in self.vendors.values() if v.status == Status.AT_RISK]

        report = []
        report.append("=" * 50)
        report.append("VENDOR ONBOARDING: WEEKLY STAKEHOLDER UPDATE")
        report.append("=" * 50)
        report.append(f"Total Vendors in Pipeline: {len(self.vendors)}")
        report.append(f"Successfully Live: {live_count}")
        report.append(f"Blocked: {len(blocked_vendors)} | At Risk: {len(at_risk_vendors)}\n")

        report.append("--- ACTION REQUIRED (BLOCKED) ---")
        if blocked_vendors:
            for v in blocked_vendors:
                report.append(f"[!] {v.name} | Owner: {v.current_owner()} | Time in Stage: {v.days_in_current_stage()} days")
                report.append(f"    Reason: {v.blocker_notes}")
        else:
            report.append("No blocked vendors. All pipelines flowing.")

        report.append("\n--- PIPELINE DISTRIBUTION ---")
        dist = {stage.value: 0 for stage in OnboardingStage}
        for v in self.vendors.values():
            dist[v.stage.value] += 1

        for stage_name, count in dist.items():
            report.append(f" - {stage_name}: {count} vendors")

        report.append("\n" + "=" * 50)
        return "\n".join(report)


# ==========================================
# 4. EXECUTION / SIMULATION (Timeline & Scale)
# ==========================================
def simulate_pipeline():
    """Simulates the 12 parallel vendors described in launch_timeline.md."""
    engine = VendorOnboardingEngine()

    brands = [
        "UrbanStyle", "LuxeWear", "StreetKing", "Minimalist.co", "DenimPro",
        "ActiveGear", "FormalEdge", "MonsoonFits", "EcoWeave", "VintageVibe",
        "NeoClassic", "TrendSetter",
    ]

    for i, brand in enumerate(brands):
        vendor = Vendor(vendor_id=f"VND-{100+i}", name=brand, sku_count=random.randint(50, 500))

        # Simulate different stages of the timeline for the 12 parallel tracks
        rand_stage = random.choice(list(OnboardingStage))
        vendor.stage = rand_stage

        # Artificially inject SLA breaches for simulation purposes
        if i % 4 == 0:
            vendor.date_entered_current_stage -= datetime.timedelta(days=6)

        engine.add_vendor(vendor)

    # Run automated QA gates on vendors currently in QA
    for vendor in engine.vendors.values():
        if vendor.stage == OnboardingStage.QA_REVIEW:
            engine.run_catalog_qa_gate(vendor.vendor_id)

    # Generate the stakeholder status report
    print(engine.generate_stakeholder_report())


if __name__ == "__main__":
    simulate_pipeline()
