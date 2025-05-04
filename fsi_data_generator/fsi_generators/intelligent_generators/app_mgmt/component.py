import random
from typing import Dict, Any

import anthropic

from data_generator import DataGenerator
from ...helpers import generate_unique_json_array
from .enums import ComponentType


def generate_random_component(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random app_mgmt component record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (app_mgmt_component_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated component data (without ID fields or FK fields)
    """
    # Define mappings of vendors to their components by component type
    vendor_component_mappings = {
        # JAVA_LIBRARY
        "Java Libraries": {
            "Apache": [
                "Commons Collections", "Commons IO", "Commons Lang", "Commons Codec", "Commons CLI",
                "Commons Math", "Commons Net", "Commons DBCP", "Commons Pool", "Commons Configuration",
                "Commons Validator", "Commons FileUpload", "Commons Text", "Log4j", "HttpClient",
                "Tomcat JDBC", "Kafka Client", "Lucene Core", "PDFBox", "POI"
            ],
            "Spring": [
                "Spring Core", "Spring Context", "Spring Beans", "Spring AOP", "Spring JDBC",
                "Spring ORM", "Spring Web", "Spring WebMVC", "Spring Security Core", "Spring Data Commons",
                "Spring Data JPA", "Spring Boot Starter", "Spring Boot Autoconfigure", "Spring Cloud Config",
                "Spring Cloud Netflix", "Spring Kafka", "Spring AMQP", "Spring Integration", "Spring Batch"
            ],
            "Oracle": [
                "Java Development Kit", "Java Runtime Environment", "JavaFX", "Coherence", "GraalVM",
                "Helidon", "Oracle JDBC Driver", "Java EE API", "Jersey", "Project Reactor"
            ],
            "Red Hat": [
                "Hibernate Core", "Hibernate Validator", "Hibernate OGM", "Hibernate Search",
                "RESTEasy", "Narayana", "Undertow", "Drools", "Infinispan", "Hawkular"
            ],
            "Eclipse Foundation": [
                "Eclipse Collections", "Eclipse JGit", "Eclipse EMF", "Eclipse Jetty", "Eclipse JAX-RS",
                "Eclipse Persistence", "Eclipse JNoSQL", "Eclipse Vert.x", "Eclipse MicroProfile", "Eclipse JPA"
            ],
            "JetBrains": [
                "Kotlin Standard Library", "Kotlin Coroutines", "Kotlin Serialization", "Exposed", "Ktor",
                "JetBrains Annotations", "JetBrains Markdown", "Kotlin Test", "Kotlin Reflect", "Kotlin Logging"
            ]
        },

        # NPM_PACKAGE
        "NPM Packages": {
            "Facebook": [
                "React", "React DOM", "React Router", "Redux", "Flux", "Jest", "Flow", "GraphQL",
                "Relay", "React Native", "Immutable.js", "Draft.js", "Create React App", "Recoil",
                "React Testing Library"
            ],
            "Google": [
                "Angular Core", "Angular Common", "Angular Forms", "Angular Router", "Angular Material",
                "Firebase", "Polymer", "Lit", "Workbox", "Closure Compiler", "Protobuf.js"
            ],
            "OpenJS Foundation": [
                "jQuery", "Lodash", "Express", "Winston", "Moment", "Mocha", "ESLint", "Webpack",
                "Node-RED", "Grunt", "Chai", "Yeoman", "RequireJS", "QUnit", "Appium"
            ],
            "Vercel": [
                "Next.js", "SWR", "Styled JSX", "Vercel CLI", "Edge Config", "Hyper", "Micro",
                "Serve", "ncc", "ms", "uid", "async-retry", "arg", "email-prompt"
            ],
            "Palantir": [
                "Blueprint", "TSLint", "Plottable", "Atlaskit", "react-mosaic", "typescript-service",
                "svg-icon-system", "grunt-tslint", "tslint-react", "stylelint-config-palantir"
            ],
            "npm": [
                "npm CLI", "npx", "libnpmaccess", "libnpmpublish", "npm-packlist", "npm-audit-report",
                "normalize-package-data", "read-package-json", "npm-profile", "pacote"
            ]
        },

        # NUGET_PACKAGE
        "NuGet Packages": {
            "Microsoft": [
                "EntityFramework", "Newtonsoft.Json", "System.Data.SqlClient", "Microsoft.AspNetCore",
                "Microsoft.Extensions.DependencyInjection", "Microsoft.Extensions.Configuration",
                "Microsoft.Extensions.Logging", "Microsoft.NET.Test.Sdk", "Microsoft.Identity.Client",
                "Microsoft.Azure.Cosmos", "Microsoft.EntityFrameworkCore", "Microsoft.ML", "Microsoft.FASTER",
                "Microsoft.Graph", "Microsoft.ApplicationInsights"
            ],
            "JetBrains": [
                "JetBrains.Annotations", "JetBrains.ReSharper.CommandLineTools", "JetBrains.dotCover.CommandLineTools",
                "JetBrains.dotMemory.Console", "JetBrains.dotTrace.CommandLineTools",
                "JetBrains.TeamCity.ServiceMessages"
            ],
            "Telerik": [
                "Telerik.UI.for.AspNet.Core", "Telerik.UI.for.Blazor", "Telerik.UI.for.WPF",
                "Telerik.UI.for.Silverlight",
                "Telerik.UI.for.Xamarin", "Telerik.Reporting", "Telerik.Windows.Controls", "Telerik.DataAccess"
            ],
            "NLog": [
                "NLog", "NLog.Config", "NLog.Schema", "NLog.Web", "NLog.Extensions.Logging",
                "NLog.MailKit", "NLog.Windows.Forms", "NLog.Database", "NLog.Targets.Syslog"
            ],
            "Serilog": [
                "Serilog", "Serilog.Sinks.Console", "Serilog.Sinks.File", "Serilog.Sinks.Async",
                "Serilog.Extensions.Logging", "Serilog.Formatting.Compact", "Serilog.Sinks.Seq",
                "Serilog.Settings.Configuration", "Serilog.Enrichers.Thread", "Serilog.Enrichers.Environment"
            ]
        },

        # PYTHON_MODULE
        "Python Modules": {
            "Python Software Foundation": [
                "requests", "urllib3", "pip", "setuptools", "wheel", "virtualenv", "coverage",
                "pytest", "mock", "six", "nose", "tox", "sphinx", "twisted", "ipython"
            ],
            "Pallets": [
                "Flask", "Jinja2", "Werkzeug", "Click", "ItsDangerous", "MarkupSafe",
                "Lektor", "Babel", "Flask-SQLAlchemy", "Flask-WTF"
            ],
            "Django Software Foundation": [
                "Django", "Django REST Framework", "Channels", "Django Debug Toolbar",
                "Django Extensions", "Django Filter", "Django Allauth", "Django MPTT",
                "Django Crispy Forms", "Django CMS"
            ],
            "NumFOCUS": [
                "NumPy", "Pandas", "Matplotlib", "SciPy", "Jupyter", "Dask", "Bokeh",
                "SymPy", "scikit-learn", "scikit-image", "Numba", "PyMC"
            ],
            "Google": [
                "TensorFlow", "Protobuf", "Absl-py", "gRPC", "googleapis-common-protos",
                "TensorBoard", "Keras", "BERT", "Dopamine", "JAX"
            ],
            "Facebook": [
                "PyTorch", "Detectron2", "Hydra", "Fairseq", "FBGEMM", "Torchvision",
                "ParlAI", "Prophet", "FAISS", "XFormers"
            ]
        },

        # RUBY_GEM
        "Ruby Gems": {
            "Rails Core Team": [
                "Rails", "ActiveRecord", "ActiveSupport", "ActiveJob", "ActionPack",
                "ActionMailer", "ActionCable", "ActionStorage", "ActionText", "Railties"
            ],
            "Shopify": [
                "Liquid", "Dashing", "Identity_Cache", "Spy", "BuildkiteRuby",
                "shopify_api", "shopify_app", "shopify_theme", "active_fulfillment", "active_shipping"
            ],
            "GitHub": [
                "Octokit", "GitHub-Markdown", "Linguist", "Scientist", "ActiveMerchant",
                "GraphQL-Client", "Sawyer", "Erubis", "Gemoji", "MiniProfiler"
            ],
            "Square": [
                "Square SDK", "RSpec", "Rack", "Nokogiri", "Puma", "Sinatra",
                "DevUtils", "KochavaTracker", "Reactor", "Heroku"
            ],
            "JetBrains": [
                "TeamCity", "RubyMine Plugin SDK", "Ruby IntelliJ IDEA Core", "JetBrains RubyScript",
                "TeamCity Rake Runner Plugin", "TeamCity Ruby Plugin", "RubyMotion Support",
                "JetBrains ActiveRecord Support"
            ]
        },

        # FRAMEWORK
        "Frameworks": {
            "Spring": [
                "Spring Framework", "Spring Boot", "Spring Cloud", "Spring Security",
                "Spring Data", "Spring Integration", "Spring Batch", "Spring Session",
                "Spring for GraphQL", "Spring HATEOAS"
            ],
            "Microsoft": [
                ".NET Framework", ".NET Core", "ASP.NET", "ASP.NET Core", "Entity Framework",
                "Blazor", "Xamarin", "MAUI", "WPF", "UWP"
            ],
            "Google": [
                "Angular", "Flutter", "Material Design", "Polymer", "Firebase",
                "Dart", "Android SDK", "Web Components", "Lit", "Google Cloud SDK"
            ],
            "Facebook": [
                "React", "React Native", "Relay", "Flux", "Redux",
                "Jest", "GraphQL", "Metro", "Hermes", "Create React App"
            ],
            "Apache": [
                "Hadoop", "Spark", "Kafka", "Struts", "Cordova",
                "CouchDB", "Mesos", "Storm", "ZooKeeper", "Cassandra"
            ],
            "JetBrains": [
                "Kotlin", "Ktor", "IntelliJ Platform", "TeamCity", "Compose Multiplatform",
                "Exposed", "MPS", "Qodana", "Space", "YouTrack"
            ]
        },

        # API
        "APIs": {
            "Stripe": [
                "Payments API", "Billing API", "Connect API", "Terminal API", "Issuing API",
                "Sigma API", "Atlas API", "Checkout API", "Identity API", "Relay API"
            ],
            "Twilio": [
                "SMS API", "Voice API", "Video API", "Chat API", "WhatsApp API",
                "Email API", "Verify API", "Programmable Wireless API", "TaskRouter API", "Sync API"
            ],
            "Salesforce": [
                "REST API", "SOAP API", "Bulk API", "Metadata API", "Streaming API",
                "Apex API", "Chatter API", "Analytics API", "Commerce API", "Connect API"
            ],
            "Google": [
                "Maps API", "Cloud API", "YouTube API", "Gmail API", "Calendar API",
                "Drive API", "Sheets API", "Analytics API", "Ads API", "Search Console API"
            ],
            "Microsoft": [
                "Microsoft Graph API", "Azure REST API", "Office 365 API", "Dynamics 365 API", "Bing API",
                "Windows API", "OneDrive API", "Outlook API", "Teams API", "SharePoint API"
            ],
            "Amazon Web Services": [
                "EC2 API", "S3 API", "DynamoDB API", "Lambda API", "SQS API",
                "SNS API", "CloudFormation API", "IAM API", "Route 53 API", "CloudWatch API"
            ],
            "Financial": {
                "Plaid": [
                    "Plaid Link API", "Transactions API", "Auth API", "Balance API", "Identity API",
                    "Assets API", "Investments API", "Liabilities API", "Income API", "Deposit Switch API"
                ],
                "SWIFT": [
                    "SWIFT MT API", "SWIFT MX API", "SWIFT gpi API", "SWIFT KYC API", "SWIFT Sanctions Screening API",
                    "SWIFT Translator API", "SWIFT FileAct API", "SWIFT InterAct API", "SWIFT Compliance Analytics API",
                    "SWIFT RMA API"
                ],
                "Mastercard": [
                    "Payment Gateway API", "Mastercard Send API", "Loyalty API", "Places API", "Rewards API",
                    "Digital Enablement API", "Customer Authentication API", "Safety Alliance API",
                    "Merchant Identifier API", "Blockchain API"
                ]
            }
        },

        # DOTNET_ASSEMBLY
        "DotNet Assemblies": {
            "Microsoft": [
                "System.Runtime", "System.Collections", "System.IO", "System.Net.Http", "System.Linq",
                "System.Text.Json", "System.Threading", "System.Security", "System.Reflection", "System.Xml",
                "System.ComponentModel", "System.Diagnostics", "System.Configuration", "System.Web",
                "System.Windows.Forms"
            ],
            "Telerik": [
                "Telerik.WinControls", "Telerik.Web.UI", "Telerik.Windows.Documents", "Telerik.Windows.Controls",
                "Telerik.Xamarin.Forms", "Telerik.Windows.Persistence", "Telerik.Web.Mvc", "Telerik.Reporting"
            ],
            "JetBrains": [
                "JetBrains.ReSharper.Psi", "JetBrains.ReSharper.Features", "JetBrains.Rider.Core",
                "JetBrains.Platform.Core", "JetBrains.Platform.Shell", "JetBrains.Annotations"
            ],
            "Syncfusion": [
                "Syncfusion.Grid.Windows", "Syncfusion.Chart.Windows", "Syncfusion.Edit.Windows",
                "Syncfusion.Tools.Windows", "Syncfusion.Shared.Base", "Syncfusion.Core", "Syncfusion.GridCommon"
            ],
            "DevExpress": [
                "DevExpress.XtraGrid", "DevExpress.XtraCharts", "DevExpress.XtraEditors", "DevExpress.Data",
                "DevExpress.Utils", "DevExpress.XtraBars", "DevExpress.XtraLayout", "DevExpress.BonusSkins"
            ]
        },

        # DOCKER_IMAGE
        "Docker Images": {
            "Docker Inc": [
                "Alpine", "Ubuntu", "Debian", "Redis", "Nginx",
                "PostgreSQL", "MariaDB", "MongoDB", "Python", "Node.js",
                "OpenJDK", ".NET SDK", "Go", "PHP", "Ruby"
            ],
            "Red Hat": [
                "RHEL", "CentOS", "Fedora", "UBI", "OpenShift",
                "JBoss", "Wildfly", "Keycloak", "Quarkus", "Infinispan"
            ],
            "Bitnami": [
                "WordPress", "Drupal", "Joomla", "Magento", "PrestaShop",
                "Moodle", "Jenkins", "SonarQube", "Grafana", "Elasticsearch"
            ],
            "Google": [
                "Distroless", "Cloud SDK", "Kubernetes", "TensorFlow", "Golang",
                "Cloud Build", "Cloud SQL Proxy", "Anthos", "Kustomize", "Skaffold"
            ],
            "HashiCorp": [
                "Consul", "Vault", "Nomad", "Terraform", "Packer",
                "Boundary", "Waypoint", "Sentinel", "Vagrant", "Envconsul"
            ],
            "Financial": {
                "FINOS": [
                    "Symphony", "Perspective", "Plexus Interop", "DataHelix", "Legend",
                    "Morphir", "Waltz", "Alloy", "Greenkey", "TimeBase"
                ],
                "Hyperledger": [
                    "Fabric", "Besu", "Sawtooth", "Indy", "Caliper",
                    "Aries", "Cactus", "FireFly", "Ursa", "Burrow"
                ]
            }
        },

        # GRADLE_PLUGIN
        "Gradle Plugins": {
            "Gradle Inc": [
                "Java", "Groovy", "Kotlin", "Application", "War",
                "Ear", "Distribution", "Publishing", "Dependencies", "Toolchains",
                "JaCoCo", "Checkstyle", "PMD", "SpotBugs", "Signing"
            ],
            "Spring": [
                "Spring Boot", "Spring Dependency Management", "Spring Cloud Contract",
                "Spring Graal Native", "Spring Asciidoctor", "Spring Javadoc"
            ],
            "JetBrains": [
                "Kotlin", "Kotlin Spring", "Kotlin JPA", "Kotlin Serialization",
                "Kotlin Multiplatform", "Compose", "Qodana"
            ],
            "Google": [
                "Android", "GCloud", "Protobuf", "JMH", "Osdetector",
                "Firebase Performance", "Firebase App Distribution", "Firebase Crashlytics"
            ],
            "Square": [
                "Sqldelight", "Wire", "OkHttp", "Retrofit", "JavaPoet",
                "KotlinPoet", "Moshi", "Anvil", "Leak Canary", "Workflow"
            ],
            "Gradle Community": [
                "Shadow", "Versions", "BuildConfig", "License Report", "Git Properties",
                "Nebula", "Spring Boot ADF", "Gradle Versions", "Dependency Updates", "Docker"
            ]
        },

        # MAVEN_PLUGIN
        "Maven Plugins": {
            "Apache": [
                "Maven Compiler", "Maven JAR", "Maven Resources", "Maven Surefire", "Maven Clean",
                "Maven Deploy", "Maven Install", "Maven Site", "Maven Dependency", "Maven Assembly",
                "Maven WAR", "Maven EAR", "Maven Javadoc", "Maven Source", "Maven Shade"
            ],
            "Spring": [
                "Spring Boot Maven", "Spring Boot Configuration Processor", "Spring Dependency Management",
                "Spring Boot Starter Parent", "Spring Cloud Contract", "Spring Milestone"
            ],
            "Codehaus": [
                "Mojo Versions", "Mojo Exec", "Mojo BuildHelper", "Mojo License", "Mojo Animal Sniffer",
                "Mojo Native", "Mojo Flatten", "Mojo Properties", "Mojo XML", "Mojo JLink"
            ],
            "SonarSource": [
                "SonarQube", "SonarJaCoCo", "SonarSCM", "SonarMaven", "SonarHTML",
                "SonarJava", "SonarXML", "SonarCSS", "SonarJS", "SonarPHP"
            ],
            "JaCoCo": [
                "JaCoCo Maven", "JaCoCo Report", "JaCoCo Agent", "JaCoCo Core", "JaCoCo CLI"
            ],
            "Financial": {
                "FinancialOSS": [
                    "ISO8583", "SWIFT MT", "SWIFT MX", "FIX Protocol", "FPML",
                    "HPAN Masking", "PCI Compliance", "AML Validation", "KYC Verification", "PSD2 Reporting"
                ]
            }
        },

        # OPERATING_SYSTEM
        "Operating Systems": {
            "Microsoft": [
                "Windows 10", "Windows 11", "Windows Server 2019", "Windows Server 2022",
                "Windows IoT", "Windows Embedded", "Windows 365", "Xbox OS"
            ],
            "Apple": [
                "macOS", "iOS", "iPadOS", "tvOS", "watchOS"
            ],
            "Google": [
                "Android", "ChromeOS", "Wear OS", "Fuchsia OS"
            ],
            "Red Hat": [
                "Red Hat Enterprise Linux", "Fedora", "CentOS"
            ],
            "Canonical": [
                "Ubuntu", "Ubuntu Server", "Ubuntu Core"
            ],
            "SUSE": [
                "SUSE Linux Enterprise Server", "SUSE Linux Enterprise Desktop", "openSUSE"
            ],
            "Oracle": [
                "Oracle Linux", "Oracle Solaris", "Java OS"
            ]
        },

        # HARDWARE_DEVICE
        "Hardware Devices": {
            "Cisco": [
                "Catalyst Switch", "Nexus Switch", "ISR Router", "ASR Router", "Firepower Firewall",
                "ASA Firewall", "UCS Server", "HyperFlex", "Meraki Access Point", "Webex Desk"
            ],
            "Dell Technologies": [
                "PowerEdge Server", "PowerVault Storage", "PowerMax Storage", "PowerStore",
                "EMC Unity", "EMC Isilon", "Dell Latitude", "Dell OptiPlex", "Dell Precision", "Dell XPS"
            ],
            "HPE": [
                "ProLiant Server", "Superdome Server", "Synergy Compute", "Alletra Storage",
                "StoreEasy Storage", "StoreOnce Backup", "Aruba Switch", "Aruba Access Point", "Aruba Controller"
            ],
            "Juniper Networks": [
                "MX Router", "EX Switch", "SRX Firewall", "QFX Switch",
                "PTX Router", "ACX Router", "NFX Series", "Junos Space", "Juniper ATP"
            ],
            "Palo Alto Networks": [
                "PA Series Firewall", "VM Series Firewall", "CN Series", "Panorama",
                "Cortex XDR", "Cortex XSOAR", "Prisma Access", "Prisma Cloud", "Prisma SD-WAN"
            ],
            "Financial": {
                "Diebold Nixdorf": [
                    "ATM", "Cash Recycler", "Teller Automation", "Self-Service Kiosk", "POS Terminal",
                    "Cash Dispenser", "Branch Transformation Device", "Vynamic Software", "AllConnect Services"
                ],
                "NCR": [
                    "NCR ATM", "NCR Self-Checkout", "NCR POS Terminal", "NCR Interactive Teller",
                    "NCR Digital Banking", "NCR Payments", "NCR Enterprise Software", "NCR Digital First Banking"
                ]
            }
        }
    }

    # Combine components by vendor across all types
    vendor_components_all = {}

    for type_group, vendors in vendor_component_mappings.items():
        if isinstance(vendors, dict):
            for vendor, components in vendors.items():
                # Special handling for nested financial vendors
                if isinstance(components, dict):
                    for fin_vendor, fin_components in components.items():
                        if fin_vendor not in vendor_components_all:
                            vendor_components_all[fin_vendor] = []
                        vendor_components_all[fin_vendor].extend(fin_components)
                else:
                    if vendor not in vendor_components_all:
                        vendor_components_all[vendor] = []
                    vendor_components_all[vendor].extend(components)

    # Map component type to appropriate vendor groups
    component_type_vendor_groups = {
        ComponentType.JAVA_LIBRARY: ["Java Libraries"],
        ComponentType.NPM_PACKAGE: ["NPM Packages"],
        ComponentType.NUGET_PACKAGE: ["NuGet Packages"],
        ComponentType.PYTHON_MODULE: ["Python Modules"],
        ComponentType.RUBY_GEM: ["Ruby Gems"],
        ComponentType.FRAMEWORK: ["Frameworks"],
        ComponentType.API: ["APIs"],
        ComponentType.DOTNET_ASSEMBLY: ["DotNet Assemblies"],
        ComponentType.DOCKER_IMAGE: ["Docker Images"],
        ComponentType.GRADLE_PLUGIN: ["Gradle Plugins"],
        ComponentType.MAVEN_PLUGIN: ["Maven Plugins"],
        ComponentType.OPERATING_SYSTEM: ["Operating Systems"],
        ComponentType.HARDWARE_DEVICE: ["Hardware Devices"]
    }

    # Get a random component type using the enum, respecting weights
    component_type = ComponentType.get_random()

    # Get applicable vendor groups for this component type
    applicable_groups = component_type_vendor_groups.get(component_type, [])

    # Collect all applicable vendors
    applicable_vendors = []
    for group in applicable_groups:
        if group in vendor_component_mappings:
            if isinstance(vendor_component_mappings[group], dict):
                applicable_vendors.extend(vendor_component_mappings[group].keys())

    # If no applicable vendors, fall back to all vendors
    if not applicable_vendors:
        applicable_vendors = list(vendor_components_all.keys())

    # Select a vendor
    vendor = random.choice(applicable_vendors)

    # Get possible components for this vendor and component type
    possible_components = []

    # Try to get components from the specific vendor and type
    for group in applicable_groups:
        if group in vendor_component_mappings:
            if isinstance(vendor_component_mappings[group], dict):
                # Check if this vendor exists in this group
                if vendor in vendor_component_mappings[group]:
                    vendor_group_components = vendor_component_mappings[group][vendor]
                    # Handle potential nested financial vendors
                    if isinstance(vendor_group_components, dict):
                        for fin_components in vendor_group_components.values():
                            possible_components.extend(fin_components)
                    else:
                        possible_components.extend(vendor_group_components)

    # If no components found, fall back to all components from this vendor
    if not possible_components and vendor in vendor_components_all:
        possible_components = vendor_components_all[vendor]

    # If still no components, select any component of the right type from any vendor
    if not possible_components:
        for group in applicable_groups:
            if group in vendor_component_mappings:
                if isinstance(vendor_component_mappings[group], dict):
                    for v_components in vendor_component_mappings[group].values():
                        # Handle potential nested financial vendors
                        if isinstance(v_components, dict):
                            for fin_components in v_components.values():
                                possible_components.extend(fin_components)
                        else:
                            possible_components.extend(v_components)

    # If we still have no components, generate a new one
    if possible_components:
        component_name = random.choice(possible_components)
    else:
        # Fallback if we couldn't find a component
        component_name = f"{vendor} {component_type.name.replace('_', ' ').title()}"

    # If we want to occasionally generate new component names that aren't in our mappings:
    if random.random() < 0.1:  # 10% chance
        try:
            new_components = generate_unique_json_array(
                dbml_string=dg.dbml,
                fully_qualified_column_name='app_mgmt.components.component_name - Common software libraries, frameworks, APIs, and modules used in financial applications including security libraries, data processing frameworks, UI components, middleware, authentication systems, and financial calculation tools',
                count=5,
                cache_key='component_names'
            )
            component_name = random.choice(new_components)

        except anthropic.APIStatusError:
            pass  # Stick with the previously selected component name

    # Generate version with semantic versioning (semver) format
    major = random.randint(0, 9)
    minor = random.randint(0, 20)
    patch = random.randint(0, 30)
    component_version = f"{major}.{minor}.{patch}"

    # For some components, add a qualifier like alpha, beta, RC
    if random.random() < 0.1:  # 10% chance
        qualifiers = ["-alpha", "-beta", "-RC1", "-RC2", "-M1", "-SNAPSHOT", "-RELEASE"]
        component_version += random.choice(qualifiers)

    # Convert component type name for display purposes (e.g., JAVA_LIBRARY to "java library")
    component_type_display = component_type.name.lower().replace('_', ' ')

    # Generate a description based on the component name and type
    descriptions = [
        f"A {component_type_display} for {component_name} that provides essential functionality for financial applications.",
        f"Official {vendor} {component_type_display} for implementing {component_name} features securely and efficiently.",
        f"Enterprise-grade {component_name} {component_type_display} with comprehensive security features.",
        f"High-performance {component_name} implementation optimized for banking applications.",
        f"{component_name} {component_type_display} that ensures compliance with financial regulations and standards.",
        f"Security-focused {component_name} that assists with GDPR, PCI-DSS, and other regulatory compliance requirements.",
        f"Scalable {component_name} implementation for handling high-volume transaction processing.",
        f"Certified {component_name} module with built-in audit logging capabilities for financial operations."
    ]
    description = random.choice(descriptions)

    # Generate package_info based on component type
    if component_type == ComponentType.JAVA_LIBRARY:
        group_id = vendor.lower().replace(" ", "").replace("-", "")
        artifact_id = component_name.lower().replace(" ", "-")
        package_info = f"{group_id}:{artifact_id}:{component_version}"
    elif component_type == ComponentType.NPM_PACKAGE:
        package_name = component_name.lower().replace(" ", "-")
        package_info = f"{package_name}@{component_version}"
    elif component_type == ComponentType.NUGET_PACKAGE:
        package_info = f"{component_name.replace(' ', '.')}.{component_version}"
    elif component_type == ComponentType.PYTHON_MODULE:
        package_info = component_name.lower().replace(" ", "_")
    elif component_type == ComponentType.RUBY_GEM:
        package_info = component_name.lower().replace(" ", "_").replace("-", "_")
    elif component_type == ComponentType.GRADLE_PLUGIN:
        package_info = f"org.{vendor.lower().replace(' ', '')}.gradle.{component_name.lower().replace(' ', '-')}"
    elif component_type == ComponentType.MAVEN_PLUGIN:
        package_info = f"org.{vendor.lower().replace(' ', '')}:maven-{component_name.lower().replace(' ', '-')}-plugin:{component_version}"
    elif component_type == ComponentType.DOCKER_IMAGE:
        package_info = f"{vendor.lower().replace(' ', '')}:{component_name.lower().replace(' ', '-')}:{component_version}"
    elif component_type == ComponentType.OPERATING_SYSTEM:
        package_info = f"{component_name} {component_version}"
    elif component_type == ComponentType.HARDWARE_DEVICE:
        package_info = f"{component_name} ({vendor})"
    else:
        package_info = f"{component_name}-{component_version}"

    # Generate repository URL based on component type
    domain = random.choice(["github.com", "gitlab.com", "bitbucket.org", "dev.azure.com"])
    org_name = vendor.lower().replace(" ", "-")
    repo_name = component_name.lower().replace(" ", "-")

    if component_type == ComponentType.JAVA_LIBRARY:
        repository_url = f"https://mvnrepository.com/artifact/{org_name}/{repo_name}"
    elif component_type == ComponentType.NPM_PACKAGE:
        repository_url = f"https://www.npmjs.com/package/{repo_name}"
    elif component_type == ComponentType.NUGET_PACKAGE:
        repository_url = f"https://www.nuget.org/packages/{component_name.replace(' ', '.')}"
    elif component_type == ComponentType.PYTHON_MODULE:
        repository_url = f"https://pypi.org/project/{repo_name}/"
    elif component_type == ComponentType.RUBY_GEM:
        repository_url = f"https://rubygems.org/gems/{repo_name}"
    elif component_type == ComponentType.DOCKER_IMAGE:
        repository_url = f"https://hub.docker.com/r/{org_name}/{repo_name}"
    elif component_type == ComponentType.GRADLE_PLUGIN:
        repository_url = f"https://plugins.gradle.org/plugin/{org_name}.{repo_name}"
    elif component_type == ComponentType.MAVEN_PLUGIN:
        repository_url = f"https://mvnrepository.com/artifact/org.{org_name}/maven-{repo_name}-plugin"
    elif component_type == ComponentType.OPERATING_SYSTEM or component_type == ComponentType.HARDWARE_DEVICE:
        repository_url = f"https://{org_name}.com/{repo_name}"
    else:
        repository_url = f"https://{domain}/{org_name}/{repo_name}"

    # Generate namespace or module
    namespace_prefixes = ["com", "org", "io", "net", "gov"]

    if component_type == ComponentType.JAVA_LIBRARY:
        namespace_or_module = f"{random.choice(namespace_prefixes)}.{org_name}.{repo_name}"
    elif component_type == ComponentType.PYTHON_MODULE:
        namespace_or_module = repo_name
    elif component_type == ComponentType.NPM_PACKAGE:
        namespace_or_module = f"@{org_name}/{repo_name}"
    elif component_type in [ComponentType.NUGET_PACKAGE, ComponentType.DOTNET_ASSEMBLY]:
        namespace_or_module = f"{vendor.replace(' ', '')}.{component_name.replace(' ', '')}"
    elif component_type == ComponentType.RUBY_GEM:
        namespace_or_module = repo_name
    elif component_type == ComponentType.GRADLE_PLUGIN:
        namespace_or_module = f"org.{org_name}.gradle.{repo_name}"
    elif component_type == ComponentType.MAVEN_PLUGIN:
        namespace_or_module = f"org.{org_name}.maven.plugins.{repo_name}"
    else:
        namespace_or_module = None

    # Generate CPE 2.3 URI based on component type
    # Format: cpe:2.3:part:vendor:product:version:update:edition:language:sw_edition:target_sw:target_hw:other

    # Determine CPE part based on component type
    cpe_part_mapping = {
        ComponentType.OPERATING_SYSTEM: "o",  # Operating System
        ComponentType.HARDWARE_DEVICE: "h",  # Hardware
    }
    cpe_part = cpe_part_mapping.get(component_type, "a")  # Default to application "a"

    # Format vendor and product appropriately for CPE
    cpe_vendor = vendor.lower().replace(" ", "_").replace("-", "_")
    cpe_product = component_name.lower().replace(" ", "_").replace("-", "_")

    # Map certain vendors to their standard CPE vendor names used in NVD
    cpe_vendor_mappings = {
        "Spring": "pivotal_software",
        "Red Hat": "redhat",
        "Microsoft": "microsoft",
        "MongoDB Inc": "mongodb",
        "JetBrains": "jetbrains",
        "HashiCorp": "hashicorp",
        "Apache": "apache",
        "Oracle": "oracle",
        "Google": "google",
        "Facebook": "facebook",
        "Eclipse Foundation": "eclipse",
        "OpenJS Foundation": "openjs",
        "Cloud Native Computing Foundation": "cncf",
        "PostgreSQL Global Development Group": "postgresql",
        "Docker Inc": "docker",
        "Kubernetes Authors": "kubernetes",
        "Elastic": "elastic",
        "Square": "square",
        "Stripe": "stripe",
        "Twilio": "twilio",
        "Grafana Labs": "grafana",
        "Datadog": "datadog",
        "New Relic": "newrelic",
        "Snyk": "snyk",
        "OWASP Foundation": "owasp",
        "Auth0": "auth0",
        "SWIFT": "swift",
        "Bloomberg LP": "bloomberg",
        "Refinitiv": "refinitiv",
        "npm": "npm",
        "Canonical": "canonical",
        "SUSE": "suse",
        "Apple": "apple",
        "Cisco": "cisco",
        "Dell Technologies": "dell",
        "HPE": "hp",
        "Juniper Networks": "juniper",
        "Palo Alto Networks": "paloalto",
        "Python Software Foundation": "python",
        "Rails Core Team": "rails",
        "Shopify": "shopify",
        "GitHub": "github",
        "Codehaus": "codehaus",
        "SonarSource": "sonarsource"
    }

    if cpe_vendor in cpe_vendor_mappings:
        cpe_vendor = cpe_vendor_mappings[cpe_vendor]

    # Use component version, but remove any leading 'v' if present and sanitize
    cpe_version = component_version
    if cpe_version.startswith("v"):
        cpe_version = cpe_version[1:]

    # For qualifiers like RC1, move them to the update field
    cpe_update = "*"
    if "-RC" in component_version:
        cpe_update = "rc" + component_version.split("-RC")[1]
        cpe_version = cpe_version.split("-RC")[0]
    elif "-M" in component_version:
        cpe_update = "m" + component_version.split("-M")[1]
        cpe_version = cpe_version.split("-M")[0]
    elif "-alpha" in component_version:
        cpe_update = "alpha"
        cpe_version = cpe_version.split("-alpha")[0]
    elif "-beta" in component_version:
        cpe_update = "beta"
        cpe_version = cpe_version.split("-beta")[0]
    elif "-SNAPSHOT" in component_version:
        cpe_update = "snapshot"
        cpe_version = cpe_version.split("-SNAPSHOT")[0]
    elif "-RELEASE" in component_version:
        cpe_update = "release"
        cpe_version = cpe_version.split("-RELEASE")[0]

    # Build the CPE 2.3 URI
    cpe23uri = f"cpe:2.3:{cpe_part}:{cpe_vendor}:{cpe_product}:{cpe_version}:{cpe_update}:*:*:*:*:*:*"

    # Create the component record
    component = {
        "component_name": component_name,
        "component_version": component_version,
        "component_type": component_type.name,
        "vendor": vendor,
        "description": description,
        "package_info": package_info,
        "repository_url": repository_url,
        "namespace_or_module": namespace_or_module,
        "cpe23uri": cpe23uri,
        "normalized_vendor": cpe_vendor
    }

    return component
