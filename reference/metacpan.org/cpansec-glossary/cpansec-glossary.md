# CPAN Security Group (CPANSec) Glossary

Source: https://security.metacpan.org/docs/glossary.html
License: CC-BY-SA-4.0

### Artifact
<a id="artifact"></a>

( SLSA-2023 ) An immutable blob of data; primarily refers to software , but SLSA can be used for any artifact. E.g. a file, a git commit, a directory of files (serialized in some way), a container image, a firmware image.

_Notes:_ Note Component and Artifact seem to some times have overlapping meaning. Recommended: Use the term Artifact specifically when referring to files, and Component in other situations. (CPANSec-2024) || See also: Component || (Ref: SLSA-2023 , CPANSec-2024 )

### Author (SBOM Role)
<a id="author-sbom-role"></a>

(NTIA-2021) An entity that creates an SBOM. author and supplier will often be different. In the case of SBOMs, the author creates the SBOM. The supplier is the provider of the software included in the SBOM.

_Notes:_ See also: Author in the Supply-chain SBOM Roles document. || (Ref: NTIA-2021 )

### Author (Project Role)
<a id="author-project-role"></a>

(CPANSec-2024) A developer that publishes something as Open Source software.

_Notes:_ (Ref: CPANSec-2024 )

### Attestation
<a id="attestation"></a>

An authenticated statement (metadata) about a software artifact or collection of software artifacts. E.g. a signed SLSA Provenance file.

_Notes:_ (Ref: SLSA-2023 )

### Build
<a id="build"></a>

(SLSA-2023) Process that transforms a set of input artifacts into a set of output artifacts. The inputs may be sources, dependencies, or ephemeral build outputs. E.g. .travis.yml (process) run by Travis CI (platform).

_Notes:_ (Ref: SLSA-2023 )

### CE Marking
<a id="ce-marking"></a>

(CRA-2024-03) A marking by which a manufacturer indicates that a product with digital elements and the processes put in place by the manufacturer are in conformity with the essential requirements set out in EU Cyber Resilience Act, Annex I and other applicable European Union harmonization legislation providing for its affixing.

_Notes:_ (Ref: CRA-2024-03 )

### Chain of custody
<a id="chain-of-custody"></a>

(SCVS-2020, CDXAG-2025 ) Auditable documentation of point of origin as well as the method of transfer from point of origin to point of destination and the identity of the transfer agent.

_Notes:_ (Ref: SCVS-2020 , CDXAG-2025 )

### Component
<a id="component"></a>

(CRA-2024-03) Software or hardware intended for integration into an electronic information system . | (NTIA-2021) A unit of software defined by a supplier at the time the component is built, packaged, or delivered. Many components contain sub-components. Examples of components include a software product, a device, a library, or a single file.

_Notes:_ Note (CPANSec) Component and Artifact seem to have overlapping definitions. Recommendation: use the term Artifact specifically when referring to files (as defined), and Component in other situations. || See also: Artifact . || (Ref: CRA-2024-03 , NTIA-2021 , CPANSec-2024 )

#### Component function
<a id="component-function"></a>

(SCVS-2020, CDXAG-2025) The purpose for which a software component exists. Examples of component functions include parsers, database persistence, and authentication providers.

_Notes:_ (Ref: SCVS-2020 , CDXAG-2025 )

#### Component, second-party
<a id="second-party"></a>

(CPANSec-2024) Any software component created and maintained through the interaction with a second party, including open source, “source available”, and proprietary software where the source is made available for either inspection, use, modification, building or sharing. Open Source software components that an application has as dependencies should be considered as “second-party” components or dependencies, since the application owner has an ongoing relationship with the FOSS component project, by the fact that the owner has accepted the open source project’s license.

_Notes:_ (Ref: CPANSec-2024 )

#### Component, third-party
<a id="third-party"></a>

(SCVS-2020) Any software component not directly created including open source, “source available”, and commercial or proprietary software. | (CPANSec-2024) Any software component not directly created including “source available”, commercial or proprietary software.

_Notes:_ See also Component, second-party . || (Ref: SCVS-2020 , CPANSec-2024 )

#### Component type
<a id="component-type"></a>

(SCVS-2020, CDXAG-2025) The general classification of a software components architecture. Examples of component types include libraries, frameworks, applications, containers, and operating systems.

_Notes:_ (Ref: SCVS-2020 , CDXAG-2025 )

### Consumer
<a id="consumer"></a>

_Notes:_ See also End-user

### CycloneDX
<a id="cyclonedx"></a>

(SCVS-2020) An OWASP managed software bill of materials specification designed to be lightweight and security-focused. CycloneDX is considered to be one of the three SBOM formats, together with SWID and SPDX .

_Notes:_ (Ref: SCVS-2020 )

### Dependency
<a id="dependency"></a>

(CPANSec-2024) A dependency is a software component that is required for another software to work as expected. This means the component which is depended upon (required) has been made available for use by the depending software so it may function as expected, without modification. Dependencies exist after they have been made available to the depending software. If a dependency is unmet (meaning – not made available, deployed, or installed), then it is called a Requirement . A dependency can come in many forms, Static, Dynamic Component, Resource or Service Vendored-in (Bundled, Embedded, Included) Peer or Plugin Direct or Transitive Optional, Virtual, Assumed (Phantom) or Unused (Zombie) In-ecosystem (Native) or Out-of-ecosystem (Non-native) Unresolved, or Resolved during Development, Development, Integration, Configuration, Build, Test, Deploy or at Runtime | (SLSA-2023) An Artifact that is an input to a build process but that is not a source. In the SLSA model, it is always a package. E.g. an Alpine package ( package ) distributed on Alpine Linux ( platform ). | ⚠️ (NTIA-2021) Characterizing the relationship that an upstream component X is included in software Y.

_Notes:_ Caution (CPANSec-2024) Dependencies may be declared/stated/referenced or included/embedded or assumed/implied/detected, development phase-specific (e.g. developer, config, build, test, deploy, or runtime-specific), dynamic or static, unresolved or resolved, direct or transitive, or required, recommended or suggested. The NTIA-2021 definition below is therefore not only wrong , but also entirely insufficient — is for any practical purpose useless and should not be used. The SLSA-2023 definition below is preferred, though it doesn’t sufficiently distinguish between stated, included and assumed dependencies. Please consider using the CPANSec-2024 definition || (Ref: SLSA-2023 , NTIA-2021 , CPANSec-2024 )

### Dependency, Direct
<a id="dependency-direct"></a>

(SCVS-2020, CDXAG-2025) A software component that is referenced by a program itself. | (CPANSec-2024) A software program, library, plugin, service, resource or component that is required for another software program or component to function as expected.

_Notes:_ See also Dependency, Transitive Dependency, Indirect || (Ref: SCVS-2020 , CDXAG-2025 , CPANSec-2024 )

#### Dependency, Development
<a id="dependency-development"></a>

(CPANSec-2024) A software or service dependency used by the component author during the development of the software. Examples: Editors, test suite data anonymisers, code generators, documentation template tools or generators, large language models

_Notes:_ Note FIXME: The name of this type of dependency isn’t clear enough! || (Ref: CPANSec-2024 ) || See also Dependency, Integration

#### Dependency, Dynamic
<a id="dependency-dynamic"></a>

_Notes:_ Note FIXME: Expand on this topic || See also Dependency, Static

#### Dependency, Indirect
<a id="dependency-indirect"></a>

(CPANSec-2024) A dependency that is used during the author, build, test or deployment stages of a program, but is is not needed any more during runtime. Examples: Compilers, test harnesses, build tooling, editors, software packaging tooling, software repositories and publishing platforms.

#### Dependency, Integration
<a id="dependency-integration"></a>

(CPANSec-2024) Software or service dependency used by the component author during any CI/CD pipeline actions, as part of the development of the software. Examples: vulnerability check actions on GitHub, commit messaging tools (like actions that report commits to an IRC channel)

_Notes:_ Note FIXME: The name of this type of dependency isn’t clear enough!

#### Dependency, Peer (Plugin, Compatibility)
<a id="dependency-peer"></a>

(CPANSec-2025) A dependency where the depending component is a plugin requiring that a compatible plugin “host” component or API is available. Original concept described in (NODEJS-2013)

_Notes:_ (Ref: CPANSec-2025 , NODEJS-2013 )

#### Dependency, Transitive
<a id="dependency-transitive"></a>

(SCVS-2020) A software component that is indirectly used by a program by means of being a dependency of a dependency. | (NTIA-2021) Characterizing the relationship that if an upstream component X is included in software Y and component Z is included in component X then component Z is included in software Y. | (CPANSec-2024) Dependencies of transitive dependencies are also transitive dependencies (it’s dependencies all the way down!).

_Notes:_ See also Dependency, Direct . || (Ref: SCVS-2020 , NTIA-2021 , CPANSec-2024 )

#### Dependency, Vendored-in (Bundled, Contained, Embedded, Included, Pre-resolved)
<a id="dependency-vendored"></a>

(CPANSec-2024) A dependency that is supplied as part of another software package, and therefore already resolved by the publisher of the package.

_Notes:_ (Ref: CPANSec-2024 )

#### Dependency, Pinned at Source
<a id="dependency-pinned-at-source-️"></a>

_Notes:_ See Dependency, Vendored-in)

#### Dependency, Resolved at Source
<a id="dependency-resolved-at-source-️"></a>

_Notes:_ See Dependency, Vendored-in

#### Dependency (Injected)
<a id="dependency-injected"></a>

(CPANSec-2024) A Dependency that is provided through other means than regular dependency resolution. e.g. A shared object library that is loaded using LD_PRELOAD . e.g. A CPAN module that is unexpectedly loaded from the current working directory in the cases when module search path @INC contains . .

#### Dependency, Phantom (Assumed, Implied, Unknown, Unstated)
<a id="dependency-phantom"></a>

(CPANSec-2024) A dependency that is used but not explicitly stated as required in the component or package metadata. A phantom dependency is a component that is required to perform an action or functionality, but has not been explicitly stated as required. An phantom dependency should be considered as a bug in the component metadata, and corrected as soon as possible. If a dependency has to be assumed or implied due to lacking capabilities in the tooling used to create the component or package, this should be considered as a bug in the tooling.

_Notes:_ Note FIXME: Expand on this topic || (Ref: CPANSec-2024 )

#### Dependency, Detected during Analysis
<a id="dependency-detected-during-analysis-️"></a>

(CPANSec-2024) A previously unknown dependency that was discovered during software dependency analysis.

_Notes:_ See Dependency Phantom (Assumed, Implied, Unknown, Unstated) || (Ref: CPANSec-2024 )

#### Dependency, Optional
<a id="dependency-optional"></a>

_Notes:_ Note FIXME: Expand on this topic || See also Dependency (Static)

#### Dependency, Unresolved (Required)
<a id="dependency-unresolved"></a>

_Notes:_ See Requirement

#### Dependency, Resolved during Configuration
<a id="dependency-configuration-time"></a>

_Notes:_ Note FIXME: Expand on this topic

#### Dependency, Resolved during Build
<a id="dependency-build-time"></a>

_Notes:_ Note FIXME: Expand on this topic

#### Dependency, Pinned during Build
<a id="dependency-build-pinned"></a>

_Notes:_ Note FIXME: Expand on this topic

#### Dependency, Resolved during Deploy
<a id="dependency-deploy-time"></a>

_Notes:_ Note FIXME: Expand on this topic

#### Dependency, Resolved at Runtime
<a id="dependency-runtime"></a>

_Notes:_ Note FIXME: Expand on this topic

#### Dependency, In-ecosystem (Native)
<a id="dependency-in-ecosystem"></a>

_Notes:_ Note FIXME: Expand on this topic || See Dependency (Out-of-ecosystem)

#### Dependency, Out-of-ecosystem (Non-native)
<a id="dependency-out-of-ecosystem"></a>

_Notes:_ Note FIXME: Expand on this topic || See also Dependency (In-ecosystem)

#### Dependency, Service
<a id="dependency-service"></a>

(CPANSec-2024) A network service dependency that are required for component to function as expected | (PCISSF-2023) Required by the PCI Software Security Framework version 1.2.1

_Notes:_ Note FIXME: Expand on this topic || (Ref: CPANSec-2024 , PCISSF-2023 )

#### Dependency, Static
<a id="dependency-static"></a>

_Notes:_ Note FIXME: Expand on this topic || See also Dependency (Dynamic)

#### Dependency, Dynamic
<a id="dependency-dynamic-1"></a>

_Notes:_ Note FIXME: Expand on this topic || See also Dependency (Static)

#### Dependency, Virtual
<a id="dependency-virtual"></a>

(CPANSec-2024) A dependency that is present, but cannot be represented by an actual software package. e.g. The OS kernel and base file-system and services that have to be in place before the first regular package may be installed.

_Notes:_ Note FIXME: Expand on this topic || (Ref: CPANSec-2024 )

#### Dependency, Zombie (Unused)
<a id="dependency-zombie"></a>

(CPANSec-2024) A dependency that has been resolved and installed, but is not in use anywhere (any more). May be a build artifact left over after earlier stages in the build process (e.g. development, configure, or testing) May be misused or exploited for downgrade attacks or expose other vulnerabilities or sensitive data. Recommended to be removed before deployment or packaging.

_Notes:_ (Ref: CPANSec-2024 )

### Requirement
<a id="requirement"></a>

(CPANSec-2024) A dependency that that needs to be resolved (be made available) for a software component to function as expected. Requirements are expected to be resolved by the Builder, Packager or Integrator of the component. An unresolved dependency has always a version constraint associated with it (implied or explicitly), to be used during dependency resolution. Also referred to as a “prereq”, “dependency”.

_Notes:_ See Also Dependency || (Ref: CPANSec-2024 )

### Pre-Requirement
<a id="pre-requirement"></a>

_Notes:_ See Requirement

### Provider (Ecosystem Role)
<a id="provider"></a>

(CPANSec-2024) The Role that is tasked with ensuring a component artifact is available for download by anyone downstream This term is in place of the term Distributor when referring to Open Source Ecosystem component suppliers. This is to disambiguate from the term Distributor in the context of the EU Cyber Resilience Act. If SBOM metadata is expected to accompany the packages or containers in question, the Provider makes sure this happens.

_Notes:_ Note Package Providers are responsible for making packages or containers that Patchers and Packagers produce, and ensure these are made available in a reliable way for downstream users, possibly in accordance with a Curator’s requirements. e.g. by setting up and managing a Debian APT repository, or a CPAN mirror, or a Docker container registry, or similar. || See also: Provider in the Supply Chain Distributor in the Supply Chain || (Ref: CPANSec-2024 , Distributor )

#### Distributor (CRA)
<a id="distributor"></a>

(CRA-2024-03) A natural or legal person in the supply chain, other than the manufacturer or the importer, that makes a product with digital elements available on the Union market without affecting its properties. | (EUBG-2022-3) The distributor is a natural or a legal person in the supply chain, other than the manufacturer or the importer, who makes a product available on the market. Distributors are subject to specific obligations and have a key role to play in the context of market surveillance.

_Notes:_ Caution (CPANSec-2024) The Cyber Resilience Act defines a distributor as someone who does not Substantially Modify a package/component. (CRA-2024-03 Article 21, 22) This means if an Importer or Distributor applies a patch with Substantial Modifications , they are to be treated as a Manufacturer , including any consequences this may entail. (CPANSec-2024) To disambiguate, we recommend Open Source Supply-chain Roles like this to be referred to as Provider || See also: Provider || (Ref: CRA-2024-03 , EUBG-2022-3 , CPANSec-2024 )

### Downstream
<a id="downstream"></a>

(NTIA-2021) Referring to how a component is subsequently used in other pieces of software at a later stage in the supply chain.

_Notes:_ (Ref: NTIA-2021 )

### Economic operator (CRA)
<a id="economic-operator-cra"></a>

(CRA-2024-03) The Manufacturer , the authorised representative, the Importer , the Distributor , or other natural or legal person who is subject to obligations in relation to the manufacture of products with digital elements or to the making available of products on the market in accordance with [the Cyber Resilience Act].

_Notes:_ (Ref: CRA-2024-03 )

### Electronic information system (CRA)
<a id="electronic-information-system-cra"></a>

(CRA-2024-03) A system, including electrical or electronic equipment, capable of processing, storing or transmitting digital data.

_Notes:_ (Ref: CRA-2024-03 )

### End-user
<a id="end-user"></a>

(NTIA-2021) Entity that obtains SBOMs. An entity can be both a supplier and consumer, using components with SBOM data in its own software, which is then passed downstream. An “end-user” consumer (that is not also a supplier) may also be called an operator or a leaf entity. | (EUBG-2022-3) The end user is any natural or legal person residing or established in the European Union, to whom a product has been made available either as a consumer outside of any trade, business, craft or profession or as a professional end user in the course of its industrial or professional activities. Many products covered by European Union product harmonisation legislation are used at work and thus also subject to Union safety at work legislation.

_Notes:_ (Ref: NTIA-2021 , EUBG-2022-3 )

### GrayPAN/GreyPAN
<a id="greypan"></a>

A GrayPAN is a publicly accessible CPAN, but published outside the CPAN infrastructure, resulting in a codebase that is factually public, but functionally non existent from the perspective of CPAN (e.g. own index). (Ref About the various PANs )

### Hardware
<a id="hardware"></a>

(CRA-2024-03) A physical electronic information system, or parts thereof capable of processing, storing or transmitting digital data.

_Notes:_ (Ref: CRA-2024-03 )

### Importer (CRA)
<a id="importer-cra"></a>

(CRA-2024-03) A natural or legal person established in the Union who places on the market a product with digital elements that bears the name or trademark of a natural or legal person established outside the European Union. | (EUBG-2022-3) The importer is a natural or legal person established in the Union who places a product from a third country on the EU market. [Their] obligations build on the obligations of the manufacturer.

_Notes:_ (Ref: CRA-2024-03 , EUBG-2022-3 )

### Life-cycle Phase
<a id="life-cycle-phase"></a>

(NTIA-2021) The stage in the software life-cycle where an SBOM is generated (e.g. from source, at the time of build or packaging, or from a built executable). | (CycloneDX-2024) Lifecycles communicate the stage(s) in which data in the BOM was captured. Different types of data may be available at various phases of a lifecycle, such as the Software Development Lifecycle (SDLC), IT Asset Management (ITAM), and Software Asset Management (SAM). Thus, a BOM may include data specific to or only obtainable in a given lifecycle. | (CPANSec-2025) The stage in a software life, from conception as an idea to deprecation and decommissioning. Many different software “stages” or “phases” can be found throughout it’s life, so calling something a “Life-cycle Phase” isn’t always easily distinguishable. Application life-cycle phases, Publishing life-cycle phases, Packaging life-cycle phases, SBOM life-cycle phases, etc.

_Notes:_ (Ref: NTIA-2021 ) || See also SBOM Types

### Making available on the market (CRA)
<a id="making-available-on-the-market-cra"></a>

(CRA-2024-03) The supply of a product with digital elements for distribution or use on the European Union market in the course of a commercial activity, whether in return for payment or free of charge. | (EUBG-2022-2, Chapter 2.2) A product is made available on the market when supplied for distribution, consumption or use on the Union market in the course of a commercial activity, whether in return for payment or free of charge. The concept of making available refers to each individual product. A product is made available on the market when supplied for distribution, consumption or use on the Union market in the course of a commercial activity, whether in return for payment or free of charge. Such supply includes any offer for distribution, consumption or use on the Union market which could result in actual supply in relation to products already manufactured (e.g. an invitation to purchase, advertising campaigns).

_Notes:_ Note FIXME: Expand on this topic FIXME: Add some clarification regarding Manufacturers, Importers, Distributors and Open Source Stewards. || (Ref: CRA-2024-03 , EUBG-2022-2 )

### Manufacturer (CRA)
<a id="manufacturer-cra"></a>

(CRA-2024-03) Any natural or legal person who develops or manufactures products with digital elements or has products with digital elements designed, developed or manufactured, and markets them under his or her name or trademark, whether for payment, monetisation or free of charge. | (EUBG-2022-3, Chapter 3.1) The manufacturer is any natural or legal person who manufactures a product or has a product designed or manufactured, and places it on the market under his own name or trademark. The manufacturer is responsible for the conformity assessment of the product and is subject to a series of obligations including traceability requirements. When placing a product on the Union market, the responsibilities of a manufacturer are the same whether he is established outside the European Union or in a Member State. The manufacturer must cooperate with the competent national authorities in charge of market surveillance in case of a product presenting a risk or being non-compliant.

_Notes:_ (Ref: CRA-2024-03 , EUBG-2022-3 )

### Open-source software
<a id="open-source-software"></a>

(NTIA-2021) Software that can be accessed, used, modified, and shared by anyone.

_Notes:_ (Ref: NTIA-2021 )

### Open source software steward (CRA)
<a id="oss-steward"></a>

(CRA-2024-03) Any legal person, other than a manufacturer , which has the purpose or objective to systematically provide support on a sustained basis for the development of specific products with digital elements qualifying as free and open source software that are intended for commercial activities, and ensures the viability of those products.

_Notes:_ Note FIXME: Expand on this topic FIXME: This is a definition that was added to the CRA on 2023-12-20, meaning it may change in the final version of the regulation. || (Ref: CRA-2024-03 )

### Package
<a id="package"></a>

(SLSA-2023) [An] Artifact that is “published” for use by others. In the model, it is always the output of a build process, though that build process can be a no-op. E.g. a Docker image (package) distributed on DockerHub (platform). E:g. a ZIP file containing source code is a package, not a source, because it is built from some other source, such as a git commit. | (CPANSec-2024) An identifiable unit of software intended for distribution, ambiguously meaning either an “artifact” or a “package name”. Only use this term when the ambiguity is acceptable or desirable.

_Notes:_ (Ref: SLSA-2023 , CPANSec-2024 )

### Package manager
<a id="package-manager"></a>

(SCVS-2020, CDXAG-2025) A distribution mechanism that makes software artifacts discoverable by requesters. | (CPANSec-2024) A distribution mechanism that makes software artifacts discoverable and installable by users of a specific package ecosystem.

_Notes:_ (Ref: SCVS-2020 , CDXAG-2025 , CPANSec-2024 )

### Package URL (PURL)
<a id="purl"></a>

(SCVS-2020, CDXAG-2025) An ecosystem-agnostic specification which standardizes the syntax and location information of software components. (CPANSec-2024) The PURL spec can be found in GitHub . As it is an open source project it is constantly evolving.

_Notes:_ (Ref: SCVS-2020 , CDXAG-2025 , CPANSec-2024 )

### Pedigree
<a id="pedigree"></a>

(SCVS-2020, CDXAG-2025) Data which describes the lineage and/or process for which software has been created or altered. | (NTIA-2021) Data on the origins of components that have come together to make a piece of software and the process under which they came together. This could include data beyond the minimum elements, such as compiler details and settings.

_Notes:_ (Ref: SCVS-2020 , CDXAG-2025 , NTIA-2021 )

### Placing on the market (CRA)
<a id="placing-on-the-market-cra"></a>

(CRA-2024-03) The first making available of a product with digital elements on the Union market. | (EUBG-2022-2, Chapter 2.3) A product is placed on the market when it is made available for the first time on the Union market. According to Union harmonisation legislation, each individual product can only be placed once on the Union market. * Products made available on the market must comply with the applicable Union harmonisation legislation at the moment of placing on the market.

_Notes:_ (Ref: CRA-2024-03 , EUBG-2022-2 )

### Point of origin
<a id="point-of-origin"></a>

(SCVS-2020, CDXAG-2025) The supplier and associated metadata from which a software component has been procured, transmitted, or received. Package repositories, release distribution platforms, and version control history are examples of various points of origin. | (CPANSec-2024) Discouraged term – Confusing definition, having common meaning with both Source , Manufacturer and Distributor .

_Notes:_ (Ref: SCVS-2020 , CDXAG-2025 , CPANSec-2024 )

### Presumption of Conformity (CRA)
<a id="presumption-of-conformity-cra"></a>

(EUBG-2022-4, Chapters 4.1.2.2, 4.1.2.3) The terms ‘standard’, ‘national standard’, ‘European standard’, ‘harmonised standard’ and ‘international standard’ are subject to concrete definitions in Article 2 of Regulation (EU) No 1025/2012. Standards are technical specifications and are therefore useful and effective in promoting and disseminating good technical practises and technical solutions. Standards are in themselves of voluntary application. Harmonised standards are European standards adopted on the basis of a request made by the Commission for the application of Union harmonisation legislation. If references of harmonised standards have been published in the Official Journal of the European Union (OJEU), they provide a presumption of conformity with the essential or other legislative requirements they aim to cover.

_Notes:_ Caution FIXME: Find a better definition! The one in the Blue Guide is more of an explanation with context. In the meantime, please read the Blue Guide text. || (Ref: CRA-2024-03 , EUBG-2022-4 )

### Procurement
<a id="procurement"></a>

(SCVS-2020, CDXAG-2025) The process of agreeing to terms and acquiring software or services for later use. (CPANSec-2024) This includes agreeing to Open Source licenses.

_Notes:_ (Ref: SCVS-2020 , CDXAG-2025 , CPANSec-2024 )

### Product
<a id="product"></a>

(CPANSec-2024) A release of a project codebase that has been made ready for easy deployment and use, and that is made available, marketed or sold with a recognizable name or trademark. Please note that a Product is distinct from a Project , in that a Product’s technology, creation, maintenance, sustainability or governance is not central factors during procurement. If a Product’s technology, creation, maintenance, sustainability or governance is in-scope during procurement, then one should instead consider the underlying Project for these selection criteria.

_Notes:_ See also: Project || (Ref: CPANSec-2024 )

### Product with digital elements (CRA)
<a id="pde"></a>

(CRA-2024-03) A software or hardware product and its Remote Data Processing solutions, including software or hardware components being placed on the market separately.

_Notes:_ (Ref: CRA-2024-03 )

### Project
<a id="project"></a>

(CPANSec-2024) the social and technical organization around a codebase which works on and decides how it is developed over time. A project has a name, a maintainer and a repository for collaboration, and may have one or more co-maintainers (possibly constituting a “core” of the Project) that help take care of the codebase. Other important features include the Project’s license, governance structures, language, ecosystem, community and culture. If the Project’s license is recognized by the Open Source Initiative as an Open Source license, then the project is an Open Source Project.

_Notes:_ (Ref: CPANSec-2024 )

### Project Roles
<a id="project-roles"></a>

_Notes:_ These are roles that may be found in Open Source projects.

#### Project Lead (Project Role)
<a id="project-lead"></a>

A person who is in charge of a project. | (CPANSec-2024) Discouraged, due to lack of precision and confusion with common usage i commercial settings. Instead, use terms like Author , Maintainer or Owner .

_Notes:_ (Ref: CPANSec-2024 )

#### Release Manager (Project Role)
<a id="release-manager-project-role"></a>

_Notes:_ Note FIXME: Expand on this topic

#### Contributor (Project Role)
<a id="packager"></a>

_Notes:_ Note FIXME: Expand on this topic

#### Packager (Project Role)
<a id="packager"></a>

_Notes:_ Note FIXME: Expand on this topic

#### Custodian (Project Role)
<a id="custodian"></a>

(CPANSec-2024) A role that operates as a temporary replacement of a Maintainer , or Owner , or works on their behalf in the case they are not available, or the project does not have any. Operates on behalf of a Maintainer in a Language Ecosystem or Package Ecosystem . A type of low-effort Maintainer with reduced responsibilities, working as a stand-in of the actual Maintainer. Cares about the continued security posture of the project. Concerned mostly with updating dependencies or applying security fixes. * May step in on behalf of the Maintainer on behalf of the Language Ecosystem or Package Ecosystem where the component is published. * May step in on behalf of the Maintainer if they are unavailable or unresponsive. * May have repository commit privileges for the Maintainer ’s project. * May publish updates on behalf of the Maintainer .

### Provenance
<a id="provenance"></a>

(SCVS-2020, CDXAG-2025) The chain of custody and origin of a software component. Provenance incorporates the point of origin through distribution as well as derivatives in the case of software that has been modified. | (NTIA-2021) Data about the chain of custody of the software and all of the constituent components, potentially including data about the authors and locations from where the components were obtained. | (SLSA-2023) Attestation (metadata) describing how the outputs were produced, including identification of the platform and external parameters.

_Notes:_ (Ref: SCVS-2020 , CDXAG-2025 , NTIA-2021 , SLSA-2023 )

### Release
<a id="release"></a>

(CPANSec-2024) A named and versioned snapshot of the codebase, that is announced as suitable for general use (e.g. “is stable”), and possibly published through a public repository, a language or package ecosystem or, some other way.

_Notes:_ (Ref: CPANSec-2024 )

### Remote Data Processing (CRA)
<a id="remote-data-processing-cra"></a>

(CRA-2024-03) Data processing at a distance the software for which is designed and developed by the manufacturer, or under the responsibility of the manufacturer, and the absence of which would prevent the product with digital elements from performing one of its functions.

_Notes:_ (Ref: CRA-2024-03 )

### Repository
<a id="repository"></a>

(CPANSec-2024) The tooling, storage, services and regime used for collaborating on improving a codebase over time, either locally or remotely across a network.

_Notes:_ (Ref: CPANSec-2024 )

### Second-party component
<a id="second-party-component"></a>

_Notes:_ See Component, second-party .

### SBOM (Software Bill of Materials)
<a id="sbom"></a>

(CRA-2024-03) A formal record containing details and supply chain relationships of components included in the software elements of a product with digital elements. | (SCVS-2020) A complete, formally structured, and machine-readable inventory of all software components and associated metadata, used by or delivered with a given piece of software. | (NTIA-2021) A formal record containing the details and supply chain relationships of various components used in building software. Software developers and vendors often create products by assembling existing open source and commercial software components. The SBOM enumerates these components in a product.

_Notes:_ (Ref: CRA-2024-03 , SCVS-2020 , NTIA-2021 )

### SBOM Attributes
<a id="sbom-attributes"></a>

#### SBOM Author Name (Attribute)
<a id="sbom-author"></a>

_Notes:_ Note FIXME: Expand on this topic || (Ref: CISA-2024-9 )

#### SBOM Timestamp (Attribute)
<a id="sbom-timestamp"></a>

_Notes:_ Note FIXME: Expand on this topic || (Ref: CISA-2024-9 )

#### SBOM Type (Attribute)
<a id="sbom-type"></a>

_Notes:_ Note FIXME: Expand on this topic || (Ref: CISA-2024-9 )

#### SBOM Primary Component (Attribute)
<a id="sbom-primary-component"></a>

(CISA-2024-9) The Primary Component, or root of dependencies, is the subject of the SBOM or the foundational component being described in the SBOM. […] component attributes […] are also identified for this component, just as they are for the direct and transitive components.

_Notes:_ (Ref: CISA-2024-9 )

#### Component Name (Attribute)
<a id="component-name"></a>

_Notes:_ Note FIXME: Expand on this topic || (Ref: CISA-2024-9 )

#### Version (Attribute)
<a id="version"></a>

_Notes:_ Note FIXME: Expand on this topic || (Ref: CISA-2024-9 )

#### Supplier Name (Attribute)
<a id="supplier-name"></a>

_Notes:_ Note FIXME: Expand on this topic || (Ref: CISA-2024-9 )

#### Cryptographic Hash (Attribute)
<a id="cryptographic-hash"></a>

_Notes:_ Note FIXME: Expand on this topic || (Ref: CISA-2024-9 )

#### Unique Identifier (Attribute)
<a id="unique-identifier"></a>

_Notes:_ Note FIXME: Expand on this topic || (Ref: CISA-2024-9 )

#### Relationships (Attribute)
<a id="relationships"></a>

_Notes:_ Note FIXME: Expand on this topic || (Ref: CISA-2024-9 )

#### License (Attribute)
<a id="license"></a>

_Notes:_ Note FIXME: Expand on this topic || (Ref: CISA-2024-9 )

#### Copyright Holder (Attribute)
<a id="copyright-holder"></a>

_Notes:_ Note FIXME: Expand on this topic || (Ref: CISA-2024-9 )

### SBOM Roles
<a id="sbom-roles"></a>

(CPANSec-2024) A person, agent or actor that does something with an SBOM document, or with specific metadata attributes in an SBOM document. This may include operations like Creating, Updating, Verifying, Censoring or Sharing SBOM documents or attributes. | (CISA-2024-3) “Data is only good if it is in the hands of the right people.”

_Notes:_ (Ref: CISA-2024-3 )

#### SBOM Assembler (Role)
<a id="sbom-assembler-role"></a>

(CPANSec-2024) An 🟨 SBOM Contributor (Non-authoritative metadata provider) that produces an SBOM that contains any resolved dependencies as part of a build, packaging or container assembly process. MAY consume Source SBOM , Build SBOM and/or Deployed SBOM type documents SHOULD produce Build SBOM and/or Deployed SBOM type documents

_Notes:_ (Ref: CPANSec-2024 )

#### SBOM Author (Authoritative Metadata provider) (Role)
<a id="sbom-author-role"></a>

(CPANSec-2024) 🟥 SBOM Author (Authoritative). An authoritative source of an SBOM, or an SBOM metadata attributes. | (CISA-2024-3) Creates an SBOM. | (CPANSec-2024) SBOM Authors create, define, or sign SBOM metadata — They make sure the attributes and related artifacts Exist . This mostly means authoritative metadata attributes as laid out in the different Supply-chain Roles . In addition to attributes encountered throughout the supply-chain, they care about the attributes listed in the table below. They may edit SBOM files manually or use tooling for analyzing artifacts, or ideally – use have SBOMs generated automatically as part of a build process. (NTIA-2021, “Produce” category)

_Notes:_ Note (CPANSec-2024) SBOM Authors who are not authoritative sources, but instead gather SBOM metadata from different dependencies, may be referred to as an SBOM Assembler . (CPANSec-2024) SBOM Authors may also collect, assemble, update, or annotate SBOM metadata — They make sure the metadata and related artifacts are Current . They may for example collect SBOMs throughout build dependency resolution, and assemble (merge), translate (transform), to produce SBOMs for analysis or audit purposes. (NTIA-2021, “Transform” category, paraphrased) (CPANSec-2024) An SBOM Author who is tasked with removing (censoring) sensitive information from SBOM documents may be called SBOM Censor || (Ref: CISA-2024-3 , NTIA-2021 , CPANSec-2024 )

#### SBOM Contributor (Non-authoritative metadata provider) (Role)
<a id="sbom-contributor-role"></a>

(CPANSec-2024) 🟨 SBOM Author (Non-authoritative) A non-authoritative SBOM Author . | (CPANSec-2024) Someone that gathers, assembles or updates SBOMs from different sources into a new SBOM. This is a informal Role separate from “SBOM Author” for clarifying the responsibility when the Role intends to gather , assemble or update metadata attributes, instead of being the authoritative creator of an attributes. This assumes some attributes may be in need of updating as an SBOM is passed down a supply-chain – for example to correct upstream assumptions like ‘Download location’, add missing attributes, or update the list of resolved dependencies. The intention is to distinguish between “SBOM Author” and “SBOM Assembler” in the same way as one distinguishes between “Create” and “Update” in CRUD – to clarify responsibilities and expectations for who is the original source of some metadata attributes.

_Notes:_ (Ref: CISA-2024-3 , NTIA-2021 , CPANSec-2024 )

#### SBOM Distributor (Role)
<a id="sbom-distributor-role"></a>

(CPANSec-2024) 🟩 SBOM Distributor. SBOM Distributor roles distribute, curate, or index SBOM metadata — They make sure the metadata and related artifacts are made Available to others . They don’t have any specific metadata attributes that are commonly used across the different supply-chain consumer roles, beyond ensuring that SBOMs are available for others to use and refer to. | (CISA-2024-3) Receives SBOMs for the purpose of sharing them with SBOM Consumers or other Distributors. | (CISA-2023) Additionally, an SBOM Distributor may care about the following activities. Discovery: Mechanism used by the consumer to know the SBOM exists and how to access it. Access: Access control mechanisms used by the author or provider to regulate who can view or use an SBOM. Transport: Mechanism provided by the author or distributor to transfer an SBOM. Also, the action of the consumer receiving an SBOM.

_Notes:_ (Ref: CISA-2023 , CISA-2024-3 , CPANSec-2024 )

#### SBOM Consumer (Role)
<a id="sbom-consumer-role"></a>

(CPANSec-2024) 🟦 SBOM Consumer. SBOM Consumer roles gather, inspect, analyze, aggregate or verify SBOM metadata — They make sure metadata and related artifacts are Useful , Complete , Correct or Compliant . They don’t have any specific metadata attributes that are commonly used across the different supply-chain Consumer roles. | (CISA-2024-3) Receives the transferred SBOM. This could include roles such as third parties, authors, integrators, and end users. | (NTIA-2021, “Consume” category) They may view SBOM files to understand the contents, and use this information to support decision making & business processes, or to compare and contrast SBOMs to discover significant changes or vulnerabilities.

_Notes:_ (Ref: CISA-2024-3 , NTIA-2021 , CPANSec-2024 )

#### SBOM Censor (Role)
<a id="sbom-censor-role"></a>

(CPANSec-2024) 🟪 SBOM Censor. An SBOM Author that removes or anonymizes sensitive metadata from an SBOM before distribution.

_Notes:_ (Ref: CPANSec-2024 )

### SBOM Types
<a id="sbom-types"></a>

(CPANSec-2024) Software Bill of Materials variations, produced under certain circumstances.

_Notes:_ (Ref: CPANSec-2024 )

#### Design SBOM (Type)
<a id="sbom-design-type"></a>

(CISA-2023) SBOM of intended, planned software project or product with included components (some of which may not yet exist) for a new software artifact.

_Notes:_ (Ref: CISA-2023 )

#### Source SBOM (Type)
<a id="sbom-source-type"></a>

(CISA-2023) SBOM created directly from the development environment, source files, and included dependencies used to build an product artifact.

_Notes:_ (Ref: CISA-2023 )

#### Build SBOM (Type)
<a id="sbom-build-type"></a>

(CISA-2023) SBOM generated as part of the process of building the software to create a releasable artifact (e.g., executable or package) from data such as source files, dependencies, built components, build process ephemeral data, and other SBOMs.

_Notes:_ (Ref: CISA-2023 )

#### Analyzed SBOM (Type)
<a id="sbom-analyzed-type"></a>

(CISA-2023) SBOM generated through analysis of artifacts (e.g., executables, packages, containers, and virtual machine images) after its build. Such analysis generally requires a variety of heuristics. In some contexts, this may also be referred to as a “3rd party” SBOM.

_Notes:_ (Ref: CISA-2023 )

#### Deployed SBOM (Type)
<a id="sbom-deployed-type"></a>

(CISA-2023) SBOM provides an inventory of software that is present on a system. This may be an assembly of other SBOMs that combines analysis of configuration options, and examination of execution behavior in a (potentially simulated) deployment environment.

_Notes:_ (Ref: CISA-2023 )

#### Runtime SBOM (Type)
<a id="sbom-runtime-type"></a>

(CISA-2023) SBOM generated through instrumenting the system running the software, to capture only components present in the system, as well as external call-outs or dynamically loaded components. In some contexts, this may also be referred to as an “Instrumented” or “Dynamic” SBOM.

_Notes:_ (Ref: CISA-2023 )

### Software
<a id="software"></a>

(CRA-2024-03) The part of an electronic information system which consists of computer code.

_Notes:_ (Ref: CRA-2024-03 )

### Software Bill of Materials (SBOM)
<a id="software-bill-of-materials"></a>

_Notes:_ See SBOM (Software Bill of Materials) .

### Software Identification (SWID)
<a id="swid"></a>

(SCVS-2020) An ISO standard that formalizes how software is tagged. SWID is considered to be one of three SBOM formats, together with CycloneDX and SPDX .

_Notes:_ (Ref: SCVS-2020 )

### Software Package Data Exchange (SPDX)
<a id="spdx"></a>

(SCVS-2020) A Linux Foundation project which produces a software bill of materials specification and a standardized list of open source licenses. SPDX is considered to be one of three SBOM formats, together with CycloneDX and SWID .

_Notes:_ (Ref: SCVS-2020 )

### Source
<a id="source"></a>

(SLSA-2023) An artifact that was directly authored or reviewed by persons, without modification. It is the beginning of the supply chain; we do not trace the provenance back any further. E.g. a git commit (source) hosted on GitHub ( platform ).

_Notes:_ (Ref: SLSA-2023 , CPANSec-2024 )

### SPDX (Software Package Data Exchange)
<a id="spdx-software-package-data-exchange"></a>

_Notes:_ See Software Package Data Exchange (SPDX) .

### Substantial Modification (CRA)
<a id="substantial-modification-cra"></a>

(CRA-2024-03) A change to the product with digital elements following its placing on the market, which affects the compliance of the product with digital elements with the essential requirements set out in the EU Cyber Resilience Act, Annex I, Part I, or which results in a modification to the intended purpose for which the product with digital elements has been assessed. Where products with digital elements are subsequently modified, by physical or digital means, in a way that is not foreseen by the manufacturer […], the modification should be considered as substantial. (CRA-2024-03, Recital 38) Security updates are not Substantial Modifications. (CRA-2024-03, Recital 39)

_Notes:_ (Ref: CRA-2024-03 )

### Supplier
<a id="supplier"></a>

(NTIA-2021) An entity that creates, defines, and identifies components and produces associated SBOMs. A supplier may also be known as a manufacturer, vendor, developer, integrator, maintainer, or provider. Ideally, all suppliers are also authors of SBOMs for the suppliers’ components. Most suppliers are also consumers. A supplier with no included upstream components is a root entity.

_Notes:_ Caution (CPANSec-2024) The term ‘Supplier’ is not well defined, and should be either avoided in favor of a more precise term, or otherwise be disambiguated. || See also Author Maintainer Manufacturer || (Ref: NTIA-2021 )

### SWID (Software Identification)
<a id="software-identification-id"></a>

_Notes:_ See Software Identification (SWID) .

### Third-party component
<a id="third-party-component"></a>

_Notes:_ See Component, third-party .

### Transitive Dependency
<a id="transitive-dependency"></a>

_Notes:_ See Dependency (Transitive)

### Vendor
<a id="vendor"></a>

