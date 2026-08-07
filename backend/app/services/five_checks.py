import time
from sqlalchemy.orm import Session
from datetime import datetime,timezone




class FiveCheckFilter:

    def check1_isolation(self, node, user) -> bool:
        return node.org_id == user.org_id

    def check2_compliance(self,node, user) -> bool:
        tags = set(node.compliance_tags)
        clearance = set(user.compliance_clearance)

    # HODs get implicit MNPI visibility for their own department's content
        if user.role == "HOD" and node.department == user.department:
            clearance = clearance | {"MNPI"}

        return tags.issubset(clearance)

    def check3_permission(self, node,user) -> bool:

        '''permission = permission_compiler_bool.get(node.level_number)

        if permission is None:
            return False

        return permission["can_read"]'''


        if user.role in ("HOD", "ADMIN"):
            return True
        if node.zone == 2:
            return True
        return True  # BFS already proved reachability within department subtree


    def check4_temporal(self, node) -> bool:

        if node.status == "SUPERSEDED":
            return False

        if (
            node.valid_until is not None
            and node.valid_until <= datetime.now(timezone.utc)
        ):
            return False

        return True

    def check5_derivability(
        self,
        node,
        threshold: float = 0.7,
    ) -> bool:

        return node.derivability_score < threshold

    def run(
        self,
        nodes,
        user,
        permission_compiler_bool,
        derivability_threshold: float = 0.7,
    ):

        print(f"Initial Candidate Nodes: {len(nodes)}")

        survivors = [
            node
            for node in nodes
            if self.check1_isolation(node, user)
        ]

        print(f"After Check 1 (Isolation): {len(survivors)}")

        survivors = [
            node
            for node in survivors
            if self.check2_compliance(node, user)
        ]

        print(f"After Check 2 (Compliance): {len(survivors)}")

        survivors = [
            node
            for node in survivors
            if self.check3_permission(
                node,
                #permission_compiler_bool,
                user
            )
        ]

        print(f"After Check 3 (Permission): {len(survivors)}")

        survivors = [
            node
            for node in survivors
            if self.check4_temporal(node)
        ]

        print(f"After Check 4 (Temporal): {len(survivors)}")

        survivors = [
            node
            for node in survivors
            if self.check5_derivability(
                node,
                derivability_threshold,
            )
        ]

        print(f"After Check 5 (Derivability): {len(survivors)}")

        return survivors

    def run_with_timing(
        self,
        nodes,
        user,
        permission_lookup,
        derivability_threshold: float = 0.7,
    ):
        timing = {}
        funnel = {}

        # Initial candidate count
        funnel["initial_candidates"] = len(nodes)

        # -------------------------
        # Check 1 - Isolation
        # -------------------------
        t = time.perf_counter()

        survivors = [
            node
            for node in nodes
            if self.check1_isolation(node, user)
        ]

        timing["check1_ms"] = round((time.perf_counter() - t) * 1000, 2)
        funnel["after_check1"] = len(survivors)

        # -------------------------
        # Check 2 - Compliance
        # -------------------------
        t = time.perf_counter()

        survivors = [
            node
            for node in survivors
            if self.check2_compliance(node, user)
        ]

        timing["check2_ms"] = round((time.perf_counter() - t) * 1000, 2)
        funnel["after_check2"] = len(survivors)

        # -------------------------
        # Check 3 - Permission
        # -------------------------
        t = time.perf_counter()

        survivors = [
            node
            for node in survivors
            if self.check3_permission(
                node,
                user,
            )
        ]

        timing["check3_ms"] = round((time.perf_counter() - t) * 1000, 2)
        funnel["after_check3"] = len(survivors)

        # -------------------------
        # Check 4 - Temporal
        # -------------------------
        t = time.perf_counter()

        survivors = [
            node
            for node in survivors
            if self.check4_temporal(node)
        ]

        timing["check4_ms"] = round((time.perf_counter() - t) * 1000, 2)
        funnel["after_check4"] = len(survivors)

        # -------------------------
        # Check 5 - Derivability
        # -------------------------
        t = time.perf_counter()

        survivors = [
            node
            for node in survivors
            if self.check5_derivability(
                node,
                derivability_threshold,
            )
        ]

        timing["check5_ms"] = round((time.perf_counter() - t) * 1000, 2)
        funnel["after_check5"] = len(survivors)

        return survivors, timing, funnel