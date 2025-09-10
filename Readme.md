# Djouman

**Cahier des charges technique (Clean Architecture) – Équipes Backend (Django), Mobile (Flutter), Web (Angular), DevOps & QA**

---

## 0) Vision & périmètre

* **Produit** : plateforme multi-acteurs (Clients, Freelances, Propriétaires/Loueurs) — web & mobile — avec authentification, réservation/mission, paiement intégré, géolocalisation, back-office.&#x20;
* **Technos retenues** :

  * **Backend** : Django + Django REST Framework (DRF)
  * **Web** : Angular
  * **Mobile** : Flutter
  * **DB** : PostgreSQL
  * **Fichiers** : S3-compatible
  * **Notifications** : FCM (push), Email (SendGrid/Mailgun), SMS (provider local)&#x20;
* **Non-objectifs** : pas de chiffrage/prix ni de durée dans ce README.

---

## 1) Rôles & cas d’usage (synthèse produit)

### 1.1 Rôles utilisateurs

* **Client** : recherche, devis, réservation, paiement, suivi, avis.
* **Freelance** : inscription/KYC, profil & services, acceptation mission, suivi (start/pause/stop), justificatifs, paiements, note moyenne.
* **Propriétaire/Loueur** : inventaire des biens/équipements, calendrier, contrats/signatures, portefeuille & statistiques.
* **Administrateur (Back-office)** : gestion des utilisateurs & contenus, validation KYC, suivi temps réel, litiges, commissions, KPIs.&#x20;

### 1.2 Parcours clés

* **Auth** (email/téléphone/OTP, reset, OAuth possible)
* **Catalogue** (catégories, filtres, géo)
* **Devis & Réservation/Mission** (workflow, calendrier, GPS/QR)
* **Paiement** (Mobile Money/Wave/Stripe) + remboursements/commissions
* **Contrats PDF** (signature) & rapports
* **Notifications** (push/email/SMS)
* **Avis/Notes**
* **Back-office** (tableau de bord, validations, litiges)&#x20;

---

## 2) Architecture globale (Clean Architecture)

### 2.1 Vue d’ensemble

* **Domain (Core)** : entités métier, interfaces (ports), règles & invariants.
* **Application (Use Cases)** : orchestration des règles, DTO, services applicatifs, validation.
* **Infrastructure** : ORM (Django models), persistance, adapters paiements, emails/sms/push, stockage fichiers, ext. API.
* **Interface (Presentation)** : API REST (DRF), web Angular, mobile Flutter, admin/back-office.

### 2.2 Frontières & dépendances

* Interface → Application → Domain (dépendance vers l’intérieur).
* Infrastructure implémente les ports définis dans Domain/Application.
* DRF expose les Use Cases via des Controllers/ViewSets minces.

---

## 3) Découpage par repositories & dossiers

### 3.1 Monorepo (recommandé)

```
djouman/
├─ backend/                # Django + DRF
├─ web/                    # Angular
├─ mobile/                 # Flutter
├─ docs/                   # ADR, schémas, OpenAPI, runbooks
├─ ops/                    # IaC, Docker, k8s manifests, GitHub Actions
└─ tools/                  # scripts, seeders, linters, hooks
```

### 3.2 Backend (Django, Clean Architecture)

```
backend/
├─ manage.py
├─ pyproject.toml / requirements.txt
├─ djouman/                            # project settings
│  ├─ __init__.py
│  ├─ settings/
│  │  ├─ base.py
│  │  ├─ local.py
│  │  ├─ staging.py
│  │  └─ production.py
│  ├─ urls.py
│  ├─ asgi.py / wsgi.py
│  └─ middleware/
│     └─ audit.py
├─ core/                               # clean layers (app boundary)
│  ├─ domain/
│  │  ├─ entities/                     # User, Profile, Service, Equipment, Booking, Mission, Payment, Payout, Dispute, Review, Commission, Organization...
│  │  ├─ value_objects/                # Money, GeoPoint, Period, Rating, Phone, Email...
│  │  ├─ events/                       # Domain events
│  │  └─ ports/                        # PaymentPort, NotificationPort, StoragePort, GeoPort, PdfPort...
│  ├─ application/
│  │  ├─ use_cases/                    # AuthUseCases, BookingUseCases, PaymentUseCases, KycUseCases...
│  │  ├─ dto/
│  │  ├─ services/                     # CommissionService, PricingService, MatchingService...
│  │  └─ validators/
│  └─ shared/
│     ├─ exceptions.py
│     ├─ utils.py
│     └─ typing.py
├─ infrastructure/
│  ├─ persistence/
│  │  ├─ models/                       # Django models
│  │  ├─ repositories/                 # ORM implementations of ports
│  │  └─ migrations/
│  ├─ providers/
│  │  ├─ payments/                     # OrangeMoneyAdapter, MTNMoMoAdapter, WaveAdapter, StripeAdapter
│  │  ├─ notifications/                # FcmAdapter, EmailAdapter, SmsAdapter
│  │  ├─ storage/                      # S3Adapter
│  │  ├─ geo/                          # GoogleMapsAdapter/OSM
│  │  └─ pdf/                          # WeasyPrint/ReportLab adapter
│  ├─ security/                        # JWT, permissions, rate limiting
│  └─ config/                          # settings helpers (env, logging)
├─ interface/
│  ├─ api/
│  │  ├─ serializers/
│  │  ├─ viewsets/                     # minces: app.use_cases.* uniquement
│  │  ├─ routers.py
│  │  └─ versioning.py
│  ├─ admin/                           # Django admin durci (lecture + opérations sûres)
│  └─ schemas/                         # OpenAPI generation
├─ tests/
│  ├─ unit/
│  ├─ application/
│  ├─ integration/
│  └─ e2e/
└─ Makefile
```

### 3.3 Web (Angular)

```
web/
├─ package.json
├─ angular.json
├─ src/
│  ├─ app/
│  │  ├─ core/             # services globaux (auth, http, interceptors, guards)
│  │  ├─ shared/           # composants/pipe/directives réutilisables
│  │  ├─ features/
│  │  │  ├─ auth/
│  │  │  ├─ catalog/
│  │  │  ├─ booking/
│  │  │  ├─ payment/
│  │  │  ├─ profile/
│  │  │  ├─ admin/         # back-office web (si besoin)
│  │  │  └─ support/       # litiges, messaging
│  │  ├─ state/             # NgRx (facultatif)
│  │  └─ app-routing.module.ts
│  ├─ environments/
│  └─ assets/
└─ tests/
```

### 3.4 Mobile (Flutter)

```
mobile/
├─ pubspec.yaml
├─ lib/
│  ├─ main.dart
│  ├─ core/                     # theme, constants, env, router
│  ├─ services/                 # http client, storage, notifications
│  ├─ features/
│  │  ├─ auth/
│  │  ├─ catalog/
│  │  ├─ booking/
│  │  ├─ payment/
│  │  ├─ profile/
│  │  └─ support/
│  ├─ widgets/                  # composants communs
│  └─ state/                    # BLoC/Riverpod
└─ test/
```

---

## 4) Modèle de données (ER — aperçu)

* **User**(id, email, phone, role, status, password\_hash, …)
* **Profile**(user\_id, name, avatar, bio, address, geo)
* **ServiceCategory**, **Service** (catalogue & tarifs)
* **Equipment**(owner\_id, photos, description, price, deposit, availability)
* **Booking**(client\_id, target: service|equipment, schedule, status, location, price, commission)
* **Mission**(freelance\_id, booking\_id, status timeline: created/accepted/started/paused/stopped/completed, gps\_track, proofs)
* **Payment**(booking\_id, method, amount, currency, fees, status, provider\_ref)
* **Payout**(beneficiary\_id, amount, status)
* **Contract**(booking\_id, file\_url, signed\_at)
* **Dispute**(booking\_id, opener, reason, messages)
* **Review**(author\_id, target\_id, rating, comment)
* **CommissionPolicy**(service\_type, rate, min/max)
  (Le détail final sera matérialisé par migrations + schéma OpenAPI/ERD.)

---

## 5) API REST (DRF) — conventions

* **Versioning** : `/api/v1/...`
* **Auth** : JWT (bearer), OTP (flow dédié), optional OAuth2.
* **Erreurs** : format `{code, message, details, trace_id}`
* **Idempotence** : `Idempotency-Key` pour endpoints sensibles (paiement/webhooks).
* **Pagination** : cursor-based par défaut.
* **Filtrage/tri** : `?filter[...]=...&sort=...`
* **Rate-limit** : par IP/compte/clé.

### 5.1 Endpoints (extrait)

* `/auth/register`, `/auth/login`, `/auth/otp/verify`, `/auth/password/reset`
* `/users/me`, `/profiles/:id`
* `/catalog/categories`, `/catalog/services`, `/equipments`
* `/bookings` (CRUD, state transitions, calendrier, QR)
* `/missions` (start/pause/stop, GPS, proofs upload)
* `/payments/intents`, `/payments/capture`, `/payments/refund`
* `/payouts`
* `/contracts` (génération PDF & signature)
* `/disputes`, `/messages`
* `/reviews`
* `/admin/*` (protégé par rôle/permissions + CSRF si session admin)

---

## 6) Intégrations externes (adapters)

* **Paiement** : Orange Money, MTN MoMo, Wave, Stripe (sandbox → prod). Ports : `PaymentPort` (`authorize/capture/refund/payout`) avec mapping statuts & webhooks idempotents.&#x20;
* **Cartographie/Géo** : Google Maps SDK ou OSM/Leaflet (geocoding, distance, itinéraire).&#x20;
* **Notifications** : FCM (push), Email (SendGrid/Mailgun), SMS (local).&#x20;
* **Stockage** : S3-compatible (presigned URLs).
* **PDF** : WeasyPrint/ReportLab pour rapports & contrats.

---

## 7) Sécurité & conformité

* **Transport** : HTTPS obligatoire, HSTS, TLS modernes.&#x20;
* **Identité** : hash Argon2/bcrypt, MFA/OTP, refresh token rotation, revoke list.
* **RBAC** : scopes par rôle (Client, Freelance, Propriétaire/Loueur, Admin).
* **Sécurité Web** : CSRF (admin), CORS strict, XSS/SQLi protections, rate-limit, CAPTCHA inscription.&#x20;
* **Audit** : journaliser actions critiques (paiement, KYC, statuts).
* **RGPD** : consentement, export/suppression, durée de rétention.&#x20;
* **Secrets** : vault (env vars chiffrées), rotation clés.

---

## 8) Environnements & DevOps

* **Envs** : `local`, `staging`, `production`.
* **CI/CD** :

  * Lint + tests (unit/integration) + build + sécurité (SAST/Dependency scan)
  * Migrations DB auto approuvées en staging, manuelles en prod
  * Déploiements : Docker + (ECS/Fargate ou k8s), RDS/PostgreSQL, S3, CloudFront/CDN
* **Observabilité** :

  * Logs structurés (JSON), corrélation `trace_id`
  * Metrics (Prometheus/OpenTelemetry) + dashboards (Grafana)
  * APM (OpenTelemetry/Jaeger)
  * Alerting (uptime, erreurs 5xx, latences, échecs paiement)
* **Backups** : snapshots DB, rotation, tests de restauration.
* **Runbooks** : incidents paiements, webhooks, files d’attente, saturation DB.

---

## 9) Qualité, QA & tests

* **Pyramide de tests** :

  * Unitaires (domain/services)
  * Application/Use Cases
  * Intégration (adapters, webhooks)
  * E2E (API + clients)
* **Contrats** : OpenAPI vérifié, Postman collection versionnée.
* **Données de démo** : fixtures/seed pour flows principaux.
* **Critères d’acceptation (Definition of Done)** :

  * Tests ≥ 80% (domain/app), zéro regression critique
  * OpenAPI & exemples Postman mis à jour
  * Logs/metrics/alerts en place
  * Accessibilité (WCAG AA) côté web
  * Performance : P95 API < 300ms pour endpoints non-IO intensifs

---

## 10) Spécifications par équipe

### 10.1 Backend (Django + DRF)

* **Livrables** :

  * Schéma DB (migrations), modèles & répos
  * Use Cases (application) + services (commission, pricing, matching)
  * Adapters : paiements (authorize/capture/refund/payout + webhooks), notifications, storage, geo, pdf
  * API DRF (viewsets/serializers) minces, JWT, throttling, versioning
  * Admin sécurisé (lecture + actions sûres), audit log
  * OpenAPI + Postman + seed
* **Points clés** :

  * Idempotence clés sur paiements & webhooks
  * Transactions DB pour changements multi-tables
  * Validation forte (DTO/serializers)
  * Éviter N+1 (select\_related/prefetch\_related)
  * Feature flags si besoin

### 10.2 Web (Angular)

* **Livrables** :

  * Shell, routing, guards (auth/role), interceptors (JWT, error)
  * Modules **Auth**, **Catalog**, **Booking**, **Payment**, **Profile**, **Support/Litiges**, **Admin** (si back-office web)
  * UI responsive (mobile-first), i18n, lazy-loading, state management (NgRx si utile)
  * Upload fichiers via presigned URLs, maps & geoloc
  * Pages d’accessibilité (form labels, focus, contrastes, ARIA)
* **Points clés** :

  * Gestion des erreurs uniforme (snackbar/toast), retry/backoff réseau
  * Garde route par rôles, déconnexion forcée si token invalide
  * Composants réutilisables (cards, list, filters)

### 10.3 Mobile (Flutter)

* **Livrables** :

  * Navigation (go\_router), thèmes, assets
  * Features **Auth**, **Catalog**, **Booking/Mission** (scan QR, GPS, états), **Payment**, **Profile**, **Support**
  * Notifications push (FCM), gestion offline (cache), file uploads
  * State (BLoC/Riverpod), http client avec interceptors JWT
* **Points clés** :

  * Permissions (location, camera) & gestion batteries
  * Écrans mission (start/pause/stop) + cartes temps réel
  * UX offline-first pour preuves & re-sync

### 10.4 Back-office (admin)

* **Livrables** :

  * Vue globale (KPIs, transactions, réservations/missions en cours)
  * CRUD utilisateurs, services, catégories
  * Workflow de **validation KYC** (freelances/propriétaires)
  * Outil de **litiges** (messagerie interne, statut)
  * **Commissions** paramétrables par service/niveau
* **Points clés** :

  * Journalisation/audit
  * Actions réversibles/sécurisées (confirmations)
  * Filtres puissants + export CSV/XLSX

### 10.5 DevOps/SecOps

* **Livrables** :

  * Dockerfiles (backend/web/mobile CI build), docker-compose local
  * Pipelines CI/CD (lint, tests, build, scan, deploy)
  * Manifests IaC (Terraform/CloudFormation)
  * Observabilité (logs/metrics/traces, dashboards, alerting)
  * Secrets management, policy IAM minimale
* **Points clés** :

  * Zéro secret en clair, rotation clés
  * Blue/green ou canary en prod
  * SLO & budgets d’erreur

### 10.6 QA

* **Livrables** :

  * Stratégie de test, cas de test, scripts E2E
  * Données de test, scénarios de non-régression
  * Tests charge/souffrance basiques (k6/Gatling)
* **Points clés** :

  * Test des parcours critiques : inscription→réservation→paiement→mission→avis
  * Tests webhooks & pannes (ré-émission, idempotence)

---

## 11) Règles de développement

* **Git** : trunk-based + feature branches ; PRs petites & fréquentes ; `conventional commits`.
* **Code style** : Black/isort/ Ruff (Python), ESLint/Prettier (TS), Dart format.
* **Revues** : checklist sécurité & perf, couverture de tests, doc à jour.
* **I18n** : FR par défaut, extensible.
* **A11y** : conformités WCAG côté web.
* **Perf** : caches (ETag, HTTP cache), pagination stricte, index DB, CDN pour assets.
* **Docs** : ADR, OpenAPI, README spécifiques par service, runbooks.

---

## 12) Checklist de livraison (MVP)

* [ ] Auth (JWT/OTP), profils & rôles
* [ ] Catalogue & recherche filtrée (catégories/services/équipements)
* [ ] Réservation/Mission (workflow complet + calendrier + QR + GPS)
* [ ] Paiement Mobile Money/Wave/Stripe (intents, capture, refund) + webhooks
* [ ] Payouts (freelance/owner)
* [ ] Contrats PDF + signature
* [ ] Notifications (push/email/sms)
* [ ] Avis/Notes
* [ ] Back-office (KYC, litiges, commissions, KPIs)
* [ ] Observabilité & sécurité (logs, APM, alertes, RBAC, audit, RGPD)
* [ ] OpenAPI + Postman + seed + e2e basiques

---

## 13) Variables d’environnement (exemple non exhaustif)

* **Backend** : `DJANGO_SECRET_KEY`, `DJANGO_SETTINGS_MODULE`, `DATABASE_URL`, `REDIS_URL`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET`, `JWT_SECRET`, `EMAIL_API_KEY`, `SMS_API_KEY`, `FCM_KEY`, `PAYMENT_{ORANGE|MTN|WAVE|STRIPE}_*`, `GOOGLE_MAPS_KEY`.
* **Web/Mobile** : `API_BASE_URL`, `MAPS_KEY`, `FCM_SENDER_ID`, etc.

---

## 14) Documentation & livrables attendus

* **OpenAPI** (`/interface/schemas/openapi.json`) + **Postman collection**
* **Guides développeurs** : démarrage local, couverture test, conventions
* **Guides Ops** : déploiement, runbooks, sauvegardes, restauration
* **Guides produit** : flux clé, rôles, matrices de permissions
* **Maquettes** (Figma) & **charte UI**
* **Données de démo** (scripts/fixtures)

---

## 15) Démarrage rapide (local)

**Backend**

```bash
cd backend
cp djouman/settings/local.example.env .env
make dev-up         # ou docker compose up -d
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Web**

```bash
cd web
npm i
npm start
```

**Mobile**

```bash
cd mobile
flutter pub get
flutter run
```

---

## 16) Annexes (références du cahier des charges reçu)

* Modules à développer côté **Client**, **Freelance**, **Propriétaire/Loueur**, **Back-office** ; intégrations **paiement/cartographie/notifications/email/SMS** ; sécurité (HTTPS, hachage, rôles, RGPD, protections XSS/CSRF/SQLi) — **conformes** à ce README.&#x20;
