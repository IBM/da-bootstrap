# Terraform Deployment Decision Guide

## Skill Overview
This skill helps Terraform template owners decide where to run their templates by evaluating the advantages and disadvantages of local versus cloud-based execution. It provides both evidence-based analysis and intent-driven decision making to accurately classify projects into one of four deployment scenarios.

## Purpose
Guide template owners through a decision-making process to select the optimal deployment approach based on their specific requirements, constraints, and objectives. This guide serves as the single source of truth for scenario classification and migration recommendations.

---

## Decision Framework

### Quick Decision Framework

#### Your Journey Path
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ SCENARIO 1  │ ──>│ SCENARIO 2  │ ──>│ SCENARIO 3  │ ──>│ SCENARIO 4  │
│   START     │    │    GROW     │    │    SCALE    │    │    SHARE    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
  Local              Cloud              Versioned          Catalog
  Development        Collaboration      Deployments        Distribution
```

#### Quick Lookup: Which Scenario Am I?

| ✓ Check Your Situation | → Your Scenario | What This Means |
|------------------------|-----------------|-----------------|
| Just testing quickly | **Scenario 1** | Run Terraform on your laptop |
| Solo work, short-term | **Scenario 1** | Keep it simple, run locally |
| Team collaboration needed | **Scenario 2** | Team works on same infrastructure together |
| Resources exist long-term (>few weeks) | **Scenario 2** | Cloud-based, protected state file |
| Need version tracking (v1.0, v2.0) | **Scenario 3** | Each deployment creates new infrastructure |
| Multiple teams need separate copies | **Scenario 3** | Everyone gets their own servers/databases |
| Template useful company-wide | **Scenario 4** | Publish globally (requires Scenario 3 first) |

**Standardized Terminology:**
- **Scenario 1: Local Development** = I run Terraform on my laptop/desktop
- **Scenario 2: Cloud Collaboration** = My team runs Terraform in the cloud, we all work on the same infrastructure
- **Scenario 3: Versioned Deployments** = Create numbered versions, each person who deploys gets their own separate servers/databases
- **Scenario 4: Catalog Distribution** = Make my template available to the whole company (requires Scenario 3 first)

---

## Hybrid Decision Process

The framework uses a two-phase approach combining automated evidence analysis with interactive intent validation:

### Phase 1: Evidence Analysis (Automated)

Scan workspace for concrete indicators:

```bash
# Check for Git repository
git remote -v
# If no output → Scenario 1

# Check for version tags
git tag -l | grep -E '^v?[0-9]+\.[0-9]+\.[0-9]+$'
# If no tags → Scenario 2
# If tags exist → Scenario 3+

# Check for catalog configuration
ls ibm_catalog.json 2>/dev/null
# If exists → Scenario 4 (ready)

# Check if published (requires IBM Cloud CLI)
ibmcloud catalog offering list --catalog "your-catalog-id"
# If listed → Scenario 4 (published)
```

### Phase 2: Intent Validation (Interactive)

Ask clarifying questions when evidence is ambiguous:

#### Scenario 1 vs 2 Decision
- "Are you testing quickly, or is this for long-term use?"
- "Will others need to manage these resources?"
- "How long will these resources exist?"

#### Scenario 2 vs 3 Decision
- "Do you need to track different versions (v1.0, v2.0)?"
- "Will multiple teams deploy separate instances?"
- "Does each deployment need independent infrastructure?"

#### Scenario 3 vs 4 Decision
- "Is this template valuable for organization-wide use?"
- "Are you ready to support other teams using this?"
- "Should this be a company standard?"

---

## Evidence + Intent Classification Matrix

| Scenario | File Evidence | Git Evidence | Intent Indicators | Validation Questions |
|----------|--------------|--------------|-------------------|---------------------|
| **1: Local Development** | `.tf` files only | No Git repo | "Just testing", "Learning", "Quick experiment" | "Is this temporary (<1 week)?" |
| **2: Cloud Collaboration** | `.tf` + Git | Git repo, no tags | "Team needs access", "Long-term resources" | "Does your team collaborate on this?" |
| **3: Versioned Deployments** | `.tf` + Git + tags | Git repo + semantic version tags | "Need versions", "Multiple deployments" | "Do teams deploy separate instances?" |
| **4: Catalog Distribution** | `.tf` + Git + tags + catalog | Git repo + tags + `ibm_catalog.json` | "Share org-wide", "Standardize patterns" | "Should everyone be able to use this?" |

### Decision Logic Flowchart

```
┌─────────────────────────────────────────────────────────────┐
│ EVIDENCE ANALYSIS                                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    Check Git Repository
                            ↓
                ┌───────────┴───────────┐
                │                       │
            No Git                  Git Exists
                │                       │
                ↓                       ↓
         SCENARIO 1          Check for Version Tags
      (Local Development)              ↓
                            ┌───────────┴───────────┐
                            │                       │
                        No Tags                 Tags Exist
                            │                       │
                            ↓                       ↓
                     SCENARIO 2          Check for ibm_catalog.json
                (Cloud Collaboration)              ↓
                                        ┌───────────┴───────────┐
                                        │                       │
                                   No Catalog              Catalog Exists
                                        │                       │
                                        ↓                       ↓
                                 SCENARIO 3              Check if Published
                          (Versioned Deployments)              ↓
                                                    ┌───────────┴───────────┐
                                                    │                       │
                                              Not Published            Published
                                                    │                       │
                                                    ↓                       ↓
                                            SCENARIO 4 (Ready)      SCENARIO 4 (Live)
                                         (Catalog Distribution)  (Catalog Distribution)
```

### Conflict Resolution Rules

When evidence and intent conflict:

1. **Evidence suggests higher scenario, intent suggests lower**: Trust intent (user may not be ready)
   - Example: Git + tags exist, but user says "just testing" → Scenario 1 or 2
   
2. **Evidence suggests lower scenario, intent suggests higher**: Recommend migration path
   - Example: No Git, but user says "team needs this" → Recommend Scenario 2 setup

3. **Ambiguous evidence**: Default to intent-based questions
   - Example: Git exists but unclear usage → Ask collaboration questions

---

## Understanding Scenario Boundaries

### Scenario 1 vs 2: Execution Location

**Key Question**: Where does Terraform run?

| Aspect | Scenario 1 | Scenario 2 |
|--------|-----------|-----------|
| Execution | Local machine | IBM Cloud Schematics |
| State File | Local file | Cloud-backed |
| Collaboration | Single user | Team access |
| Backup | Manual | Automatic |

**Transition Trigger**: When team collaboration or long-term resources are needed

### Scenario 2 vs 3: Infrastructure Sharing Model

**Key Question**: Do deployments share infrastructure or create separate instances?

**Scenario 2: Shared Infrastructure**
```
Git Repo → Schematics Workspace → ONE Infrastructure
           (Team collaborates)     (Everyone shares)
```
- One Git repository
- Team collaborates on **the same infrastructure**
- Changes affect everyone's environment
- Example: Team manages production VPC together

**Scenario 3: Versioned Templates**
```
Git Repo v1.0 → Team A Workspace → Team A Infrastructure
             ↘ Team B Workspace → Team B Infrastructure
             ↘ Team C Workspace → Team C Infrastructure
```
- One Git repository with version tags
- Each deployment creates **separate infrastructure**
- Changes don't affect other deployments
- Example: Each team deploys their own VPC from v2.1.0

**When to Transition from 2 to 3:**
- ✅ Multiple teams need the template
- ✅ Need to test new versions without affecting production
- ✅ Different teams need different configurations
- ✅ Want to track "what version is deployed where"

**When to Stay in Scenario 2:**
- ✅ Single team, single environment
- ✅ Everyone works on same infrastructure
- ✅ No need for version tracking
- ✅ Changes are coordinated

### Scenario 3 vs 4: Distribution Scope

**Key Question**: Who can access and use this template?

| Aspect | Scenario 3 | Scenario 4 |
|--------|-----------|-----------|
| Access | Team/project specific | Organization-wide |
| Discovery | Word-of-mouth | Catalog search |
| Deployment | Manual setup | One-click deploy |
| Support | Informal | Formal support model |

**Transition Trigger**: Template is mature, proven, and valuable for wider adoption

---

## Intent-Based Decision Tree

```
START: Am I just testing something quickly?
│
├─ YES → SCENARIO 1: Local Development
│         What this means: Install Terraform on your laptop, run it there
│         Good for: Quick experiments, learning, throwaway tests
│         ⚠️  Warning: Only you can manage these resources
│
└─ NO → Will other people need to work on this with me?
         OR will these resources exist for more than a few weeks?
    │
    ├─ YES → Do I need to track different versions (like v1.0, v2.0)?
    │   │
    │   ├─ NO → SCENARIO 2: Cloud Collaboration
    │   │         What this means: Team works together on the same infrastructure
    │   │         Good for: Production systems, team projects, long-term resources
    │   │         ✓ Everyone manages the same servers/databases together
    │   │
    │   └─ YES → SCENARIO 3: Versioned Deployments
    │             What this means: Create v1.0, v2.0, etc. Each person who deploys gets their own separate servers/databases
    │             Good for: Reusable templates, different environments, multiple teams
    │             ✓ Track versions, everyone gets their own independent infrastructure
    │
    │             Later, ask yourself: Should everyone in my company be able to use this?
    │             │
    │             └─ YES → SCENARIO 4: Catalog Distribution
    │                       What this means: Publish your template company-wide
    │                       Good for: Standard patterns everyone can use
    │                       ✓ Company-wide access, reduces duplicate work
    │
    └─ NO → SCENARIO 1: Local Development
              What this means: Keep it simple, run locally
              Good for: Personal projects, solo work
```

**In Plain English:**
- **Scenario 1 vs 2**: My computer vs Cloud (where does it run?)
- **Scenario 2 vs 3**: Team shares same infrastructure vs Everyone gets their own separate infrastructure
- **Scenario 3 vs 4**: Private to my team vs Available to whole company

**Important:** You must do Scenario 3 before you can do Scenario 4 - you can't share something company-wide until you've created the versioned template first.

---

## Evidence Interpretation Guide

### Workspace Scan Results

| Evidence Found | Most Likely Scenario | Confidence | Next Step |
|----------------|---------------------|------------|-----------|
| `.tf` files only, no Git | Scenario 1 | High | Confirm short-term intent |
| Git repo, no tags, no catalog | Scenario 2 | Medium* | Ask about versioning needs |
| Git repo + semantic version tags | Scenario 3 | High | Ask about sharing plans |
| Git repo + tags + `ibm_catalog.json` | Scenario 4 (ready) | High | Verify publication status |
| Published in catalog | Scenario 4 (published) | High | Provide optimization guidance |

*Medium confidence because user might be in Scenario 1 with Git for backup only.

### Additional Evidence Indicators

**Scenario 1 Indicators:**
- No `.git` directory
- State file in local directory
- No CI/CD configuration
- Single developer commits
- No documentation

**Scenario 2 Indicators:**
- Git repository exists
- No version tags
- Team collaboration in commits
- Schematics workspace configured
- Basic documentation

**Scenario 3 Indicators:**
- Semantic version tags (v1.0.0, v2.1.0)
- Release notes or CHANGELOG
- Multiple examples/flavors
- Automated testing
- Comprehensive documentation

**Scenario 4 Indicators:**
- `ibm_catalog.json` present
- Architecture diagrams
- Support documentation
- Published to catalog

---

## Automated Migration Triggers

### When to Evolve Scenarios

#### From Scenario 1 to Scenario 2

**Automatic Triggers:**
- Resources exist >2 weeks
- Second person needs access
- State file lost/corrupted
- Backup concerns arise
- Multiple commits from different authors

**Manual Triggers:**
- Team formation
- Project becomes important
- Need for audit trail
- Compliance requirements

**Agent Response Template:**
"I notice [evidence]. Your project shows signs of team collaboration. Consider migrating to Scenario 2 (Cloud Collaboration) for better state management and team access."

#### From Scenario 2 to Scenario 3

**Automatic Triggers:**
- Need to test changes without affecting production
- Multiple teams want to use template
- Different configurations needed
- Version tracking requested
- Multiple branches (dev, staging, prod)

**Manual Triggers:**
- Template becomes reusable
- Need deployment independence
- Want to track "what's deployed where"
- Multiple environments required

**Agent Response Template:**
"I see [evidence]. You might benefit from Scenario 3 (Versioned Deployments) to track releases and enable independent deployments."

#### From Scenario 3 to Scenario 4

**Automatic Triggers:**
- 10+ releases published
- Multiple teams already using it
- Documentation is comprehensive
- Template is stable and tested
- User mentions "other teams" or "company-wide"

**Manual Triggers:**
- Organization-wide value identified
- Reduce duplicate work
- Standardize patterns
- Enable self-service

**Agent Response Template:**
"Your template has [evidence]. It appears ready for Scenario 4 (Catalog Distribution). Would you like to share this organization-wide?"

---

## Local vs Cloud-Based Execution

### Local Terraform (Scenario 1)

#### Advantages
✅ **Speed & Simplicity**
- No setup required
- Instant feedback
- No network dependency
- Rapid debugging

✅ **Development Flexibility**
- Experiment freely
- Test breaking changes safely
- No impact on others
- Complete control

✅ **Cost Efficiency**
- No Schematics service costs
- No repository hosting fees
- Pay only for created resources
- Minimal overhead

✅ **Privacy**
- Code stays on local machine
- No external dependencies
- Complete isolation
- Sensitive data contained

#### Disadvantages
❌ **Single User Limitation**
- Only you can manage resources
- No team collaboration possible
- Knowledge locked to one person
- Bus factor of 1

❌ **State File Risk**
- Vulnerable to machine failure
- Risk of accidental deletion
- No automatic backups
- Corruption possible

❌ **No Disaster Recovery**
- Lost machine = lost state
- No redundancy
- Manual backup required
- Recovery difficult

❌ **Limited Scalability**
- Cannot handle team growth
- No concurrent operations
- Single point of failure
- Difficult to hand off

❌ **No Audit Trail**
- Changes not tracked
- No approval workflow
- Limited accountability
- Compliance challenges

#### Best For
- Template development and testing
- Learning Terraform
- Proof of concepts
- Short-lived resources (< 1 week)
- Personal projects
- Rapid prototyping

#### Avoid When
- Resources will exist > 1 month
- Team collaboration needed
- Production environments
- Compliance requirements exist
- Business-critical infrastructure
- Multiple people need access

### Cloud-Based Terraform (Schematics) (Scenarios 2-4)

#### Advantages
✅ **Team Collaboration**
- Multiple users can manage resources
- Shared state file access
- Collective maintenance
- Knowledge distribution

✅ **State File Protection**
- Cloud-backed storage
- Automatic backups
- Disaster recovery built-in
- Corruption protection

✅ **Reliability**
- Survives local machine failures
- No single point of failure
- High availability
- Enterprise-grade storage

✅ **Access Control**
- IAM-based permissions
- Role-based access
- Audit logging
- Compliance support

✅ **Version Control Integration**
- Git repository required
- Change tracking automatic
- Code review possible
- Rollback capability

✅ **Scalability**
- Handle large deployments
- Concurrent operations
- Team growth supported
- Enterprise-ready

#### Disadvantages
❌ **Setup Complexity**
- Git repository required
- Cloud account needed
- IAM configuration necessary
- Learning curve exists

❌ **Slower Iteration**
- Commit/push cycle required
- Workspace update needed
- Additional steps involved
- More time per change

❌ **Cost Overhead**
- Repository hosting costs (if private)
- Potential Schematics costs
- Cloud storage fees
- Management overhead

❌ **Network Dependency**
- Internet connection required
- Cloud service availability
- Potential latency
- Connectivity issues possible

❌ **Less Privacy**
- Code in repository
- State in cloud
- Logs in cloud
- More exposure points

#### Best For
- Team collaboration
- Long-term resources (> 1 month)
- Production environments
- Business-critical infrastructure
- Compliance requirements
- Shared resource management

#### Avoid When
- Quick testing only
- Single user sufficient
- No internet access
- Extreme privacy needs
- Learning/experimentation
- Disposable resources

---

## Decision Criteria Matrix

### Evaluate Your Situation

| Criterion | Scenario 1 | Scenario 2 | Scenario 3 | Scenario 4 | Weight |
|-----------|-----------|-----------|-----------|-----------|--------|
| **Team Size** | | | | | |
| Single user | ✅ Excellent | ⚠️ Overkill | ⚠️ Overkill | ❌ Unnecessary | High |
| 2-5 users | ❌ Poor | ✅ Excellent | ✅ Good | ⚠️ Optional | High |
| 5+ users | ❌ Impossible | ✅ Excellent | ✅ Excellent | ✅ Recommended | High |
| Multiple teams | ❌ Impossible | ⚠️ Difficult | ✅ Excellent | ✅ Required | Critical |
| **Resource Lifetime** | | | | | |
| < 1 day | ✅ Perfect | ⚠️ Overkill | ❌ Overkill | ❌ Unnecessary | Medium |
| 1 day - 1 week | ✅ Good | ⚠️ Optional | ❌ Overkill | ❌ Unnecessary | Medium |
| 1 week - 1 month | ⚠️ Risky | ✅ Good | ✅ Good | ⚠️ Optional | High |
| > 1 month | ❌ Dangerous | ✅ Required | ✅ Required | ✅ Recommended | Critical |
| **Environment Type** | | | | | |
| Development | ✅ Good | ✅ Good | ✅ Good | ⚠️ Optional | Low |
| Testing | ⚠️ Acceptable | ✅ Better | ✅ Better | ⚠️ Optional | Medium |
| Staging | ❌ Poor | ✅ Required | ✅ Required | ✅ Recommended | High |
| Production | ❌ Never | ✅ Required | ✅ Required | ✅ Recommended | Critical |
| **Collaboration Need** | | | | | |
| None | ✅ Perfect | ⚠️ Overkill | ⚠️ Overkill | ❌ Unnecessary | High |
| Occasional | ❌ Difficult | ✅ Good | ✅ Good | ⚠️ Optional | High |
| Frequent | ❌ Impossible | ✅ Required | ✅ Required | ✅ Recommended | Critical |
| **Version Control Need** | | | | | |
| None | ✅ Fine | ✅ Fine | ⚠️ Overkill | ❌ Unnecessary | Medium |
| Basic tracking | ⚠️ Manual | ✅ Good | ✅ Good | ⚠️ Optional | Medium |
| Formal releases | ❌ Difficult | ⚠️ Possible | ✅ Required | ✅ Required | High |
| **Distribution Scope** | | | | | |
| Personal | ✅ Perfect | ⚠️ Optional | ❌ Overkill | ❌ Unnecessary | Medium |
| Team | ❌ Poor | ✅ Good | ✅ Good | ⚠️ Optional | High |
| Multiple teams | ❌ Impossible | ⚠️ Difficult | ✅ Excellent | ✅ Recommended | High |
| Organization-wide | ❌ Impossible | ❌ Impossible | ⚠️ Possible | ✅ Required | Critical |
| **Risk Tolerance** | | | | | |
| High | ✅ Acceptable | ⚠️ Optional | ⚠️ Optional | ⚠️ Optional | Medium |
| Medium | ⚠️ Risky | ✅ Better | ✅ Better | ✅ Better | High |
| Low | ❌ Unacceptable | ✅ Required | ✅ Required | ✅ Required | Critical |
| **Compliance** | | | | | |
| None | ✅ Fine | ✅ Fine | ✅ Fine | ✅ Fine | Low |
| Internal policies | ⚠️ Check | ✅ Better | ✅ Better | ✅ Better | Medium |
| Regulatory | ❌ Likely fails | ✅ Required | ✅ Required | ✅ Required | Critical |

### Scoring Guide
- Count your ✅ (Excellent/Perfect/Required) = 3 points
- Count your ✅ (Good/Better) = 2 points
- Count your ⚠️ (Acceptable/Optional) = 1 point
- Count your ❌ (Poor/Dangerous/Never) = 0 points

**If Scenario 1 score is highest**: Start with local, plan migration
**If Scenario 2 score is highest**: Use cloud collaboration from the start
**If Scenario 3 score is highest**: Implement versioned deployments
**If Scenario 4 score is highest**: Prepare for catalog distribution
**If scores are close**: Consider hybrid approach or ask clarifying questions

---

## Migration Strategies

### From Local to Cloud (Scenario 1 → 2)

#### Strategy 1: Fresh Start (Recommended)
1. Commit template to Git
2. Create Schematics workspace
3. Deploy new resources
4. Migrate workloads
5. Destroy local resources

**Pros**: Clean state, no complications
**Cons**: Requires workload migration

#### Strategy 2: State Import
1. Commit template to Git
2. Create Schematics workspace
3. Import existing state file
4. Verify state accuracy
5. Continue management in cloud

**Pros**: Keep existing resources
**Cons**: Complex, error-prone

#### Strategy 3: Parallel Management
1. Keep local resources running
2. Create cloud resources separately
3. Gradually migrate workloads
4. Decommission local resources
5. Complete transition

**Pros**: Zero downtime
**Cons**: Temporary duplication costs

### From Cloud to Versioned (Scenario 2 → 3)

#### Strategy 1: Tag Current State
1. Create initial version tag (v1.0.0)
2. Document current deployment
3. Set up release process
4. Create examples for reuse
5. Enable independent deployments

**Pros**: Preserves existing deployment
**Cons**: Requires documentation effort

#### Strategy 2: Refactor and Release
1. Refactor for reusability
2. Create modular structure
3. Add examples and tests
4. Tag first official release
5. Enable team deployments

**Pros**: Improved template quality
**Cons**: More upfront work

### From Versioned to Catalog (Scenario 3 → 4)

#### Strategy 1: Direct Publication
1. Create `ibm_catalog.json`
2. Add comprehensive documentation
3. Set up automated releases
4. Publish to catalog
5. Announce availability

**Pros**: Fast to market
**Cons**: May need refinement

#### Strategy 2: Pilot Program
1. Create catalog configuration
2. Pilot with select teams
3. Gather feedback
4. Refine based on input
5. Full publication

**Pros**: Validated before wide release
**Cons**: Longer timeline

---

## Real-World Scenarios

### Scenario 1: Solo Developer Testing
**Situation**: Testing new Terraform module
**Evidence**: `.tf` files only, no Git
**Intent**: "Just experimenting"
**Recommendation**: Scenario 1 (Local Development)
**Reasoning**: Quick iteration needed, disposable resources, no collaboration

### Scenario 2: Team Building Shared Infrastructure
**Situation**: 5 developers building company VPC
**Evidence**: Git repo, no tags, multiple contributors
**Intent**: "Team needs to manage this together"
**Recommendation**: Scenario 2 (Cloud Collaboration)
**Reasoning**: Team collaboration essential, long-term resources, production-bound

### Scenario 3: Reusable Template Development
**Situation**: Creating template for multiple team deployments
**Evidence**: Git repo + version tags, examples directory
**Intent**: "Each team needs their own instance"
**Recommendation**: Scenario 3 (Versioned Deployments)
**Reasoning**: Multiple independent deployments, version tracking needed

### Scenario 4: Organization-Wide Standard
**Situation**: Mature template used by 10+ teams
**Evidence**: Git + tags + catalog config, comprehensive docs
**Intent**: "Make this available company-wide"
**Recommendation**: Scenario 4 (Catalog Distribution)
**Reasoning**: Proven value, ready for self-service, reduce duplication

### Scenario 5: Ambiguous Evidence
**Situation**: Git repo exists with tags, but single developer
**Evidence**: Git repo + 20 version tags
**Intent**: "Just me working on this"
**Resolution**: Scenario 3 is correct (versioning for personal use is valid)
**Agent Response**: "You're in Scenario 3. Consider Scenario 4 if others could benefit."

### Scenario 6: Premature Classification
**Situation**: Catalog file exists but no releases
**Evidence**: Git repo + `ibm_catalog.json`, no tags
**Intent**: "Preparing for future sharing"
**Resolution**: Scenario 2 (catalog file prepared but not ready)
**Agent Response**: "You have catalog config but no releases. Create version tags to reach Scenario 4."

---

## Common Mistakes to Avoid

### ❌ Using Local for Production
**Problem**: State file loss causes production outage
**Solution**: Always use cloud for production (Scenario 2+)

### ❌ Using Cloud for Quick Tests
**Problem**: Overhead slows development
**Solution**: Use local for rapid iteration (Scenario 1)

### ❌ No Migration Plan
**Problem**: Stuck with local when team grows
**Solution**: Plan cloud migration from start

### ❌ Ignoring State File Backups
**Problem**: Lost state file, unmanaged resources
**Solution**: Backup local state or use cloud

### ❌ Mixing Local and Cloud
**Problem**: State file conflicts, resource drift
**Solution**: Choose one approach per template

### ❌ Premature Catalog Publication
**Problem**: Immature template causes user issues
**Solution**: Ensure 10+ stable releases before Scenario 4

### ❌ Skipping Scenario 3
**Problem**: Can't publish to catalog without versions
**Solution**: Must implement versioning before catalog distribution

---

## Decision Checklist

Use this checklist to make your decision:

### Choose Scenario 1 (Local Development) if:
- [ ] Single user only
- [ ] Resources exist < 1 week
- [ ] Rapid iteration needed
- [ ] Learning/experimenting
- [ ] No compliance requirements
- [ ] Disposable infrastructure
- [ ] Development/testing only

### Choose Scenario 2 (Cloud Collaboration) if:
- [ ] Multiple users need access
- [ ] Resources exist > 1 month
- [ ] Production environment
- [ ] Team collaboration needed
- [ ] Compliance requirements exist
- [ ] Business-critical infrastructure
- [ ] Disaster recovery needed
- [ ] Audit trail required
- [ ] No versioning needed yet

### Choose Scenario 3 (Versioned Deployments) if:
- [ ] Multiple independent deployments needed
- [ ] Version tracking required (v1.0, v2.0)
- [ ] Different teams need separate instances
- [ ] Template is reusable
- [ ] Need to test without affecting production
- [ ] Want to track "what's deployed where"
- [ ] Multiple environments (dev/staging/prod)

### Choose Scenario 4 (Catalog Distribution) if:
- [ ] Template is mature (10+ releases)
- [ ] Multiple teams already using it
- [ ] Documentation is comprehensive
- [ ] Organization-wide value identified
- [ ] Want to enable self-service
- [ ] Reduce duplicate work
- [ ] Standardize patterns company-wide
- [ ] Ready to provide formal support

### Consider Hybrid Approach if:
- [ ] Development phase → production
- [ ] Testing locally, deploying to cloud
- [ ] Learning before production use
- [ ] Prototyping before team adoption

---

## Next Steps by Scenario

### If You Chose Scenario 1 (Local Development)
1. Review: `local-terraform-management.md`
2. Set up local Terraform
3. Plan cloud migration timeline
4. Document state file location
5. Set backup reminders

### If You Chose Scenario 2 (Cloud Collaboration)
1. Review: `cloud-schematics-terraform.md`
2. Create Git repository
3. Set up IBM Cloud account
4. Create Schematics workspace
5. Configure team access

### If You Chose Scenario 3 (Versioned Deployments)
1. Review: `terraform-product-offerings.md`
2. Implement semantic versioning
3. Create release process
4. Add examples and documentation
5. Set up automated testing

### If You Chose Scenario 4 (Catalog Distribution)
1. Review: `global-terraform-sharing.md`
2. Create `ibm_catalog.json`
3. Enhance documentation
4. Set up automated releases
5. Publish to catalog

### If You Chose Hybrid Approach
1. Start with local development (Scenario 1)
2. Review both relevant skill documents
3. Plan migration trigger points
4. Prepare Git repository
5. Document transition plan

---

## Getting Help

### Questions to Ask Yourself
1. How long will these resources exist?
2. Who needs to manage them?
3. What's the risk if state file is lost?
4. Are there compliance requirements?
5. Is this development or production?
6. How often will changes occur?
7. What's the team size?
8. Do we need version tracking?
9. Should this be shared widely?

### Decision Support
If still unsure, consider:
- **Default to Scenario 2** if any doubt about longevity
- **Start with Scenario 1** only if certain about short-term use
- **Consult team** for shared infrastructure decisions
- **Review compliance** requirements before deciding
- **Ask intent questions** when evidence is ambiguous

---

## Summary

### The Golden Rules
1. **Local for speed, Cloud for safety**
2. **Single user = Scenario 1, Team = Scenario 2+**
3. **Short-term = Scenario 1, Long-term = Scenario 2+**
4. **Development = Flexible, Production = Scenario 2+**
5. **Shared infrastructure = Scenario 2, Separate instances = Scenario 3**
6. **Team use = Scenario 3, Company-wide = Scenario 4**
7. **When in doubt, choose Cloud (Scenario 2)**
8. **Must do Scenario 3 before Scenario 4**

### Remember
- You can always migrate from local to cloud
- Migrating from cloud to local is rarely needed
- The right choice depends on your specific situation
- Consider future needs, not just current state
- State file protection is critical for long-term resources
- Evidence + Intent = Accurate classification
- Scenario boundaries are clear with the right questions

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│ SCENARIO QUICK REFERENCE                                     │
├─────────────────────────────────────────────────────────────┤
│ 1: LOCAL DEVELOPMENT                                         │
│    Evidence: .tf files, no Git                              │
│    Intent: Testing, learning, solo                          │
│    Duration: <1 week                                         │
│    State: Local file                                         │
├─────────────────────────────────────────────────────────────┤
│ 2: CLOUD COLLABORATION                                       │
│    Evidence: Git repo, no tags                              │
│    Intent: Team shares same infrastructure                  │
│    Duration: >1 month                                        │
│    State: Cloud-backed                                       │
├─────────────────────────────────────────────────────────────┤
│ 3: VERSIONED DEPLOYMENTS                                     │
│    Evidence: Git repo + version tags                        │
│    Intent: Multiple independent deployments                 │
│    Duration: Long-term, multiple instances                  │
│    State: Cloud-backed per deployment                       │
├─────────────────────────────────────────────────────────────┤
│ 4: CATALOG DISTRIBUTION                                      │
│    Evidence: Git + tags + ibm_catalog.json                  │
│    Intent: Organization-wide sharing                        │
│    Duration: Long-term, company standard                    │
│    State: Cloud-backed per deployment                       │
└─────────────────────────────────────────────────────────────┘