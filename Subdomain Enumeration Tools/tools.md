# 🎯 Subdomain Enumeration Tools


###  SubScan: Chrome Extension for subdomain enumeration

### Subdomains Generator:

```
https://husseinphp.github.io/subdomain/
```

## Bash script for subdomains:

```
#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
ORANGE='\033[38;5;208m'
PURPLE='\033[38;5;141m'
PINK='\033[38;5;206m'
LIME='\033[38;5;118m'
TEAL='\033[38;5;30m'
GOLD='\033[38;5;220m'
SILVER='\033[38;5;250m'
BRIGHT_RED='\033[1;31m'
BRIGHT_GREEN='\033[1;32m'
BRIGHT_BLUE='\033[1;34m'
BRIGHT_CYAN='\033[1;36m'
NC='\033[0m'
BOLD='\033[1m'
UNDERLINE='\033[4m'
BLINK='\033[5m'

echo -e "${CYAN}"
cat << "EOF"
    ____        __       ____             __                
   / __ \____  / /____  / __ \___  _____/ /___  _____      
  / / / / __ \/ __/ _ \/ / / / _ \/ ___/ / __ \/ ___/      
 / /_/ / /_/ / /_/  __/ /_/ /  __/ /__/ / /_/ (__  )       
/_____/\____/\__/\___/_____/\___/\___/_/\____/____/        

   🔍 Ultimate Subdomain Enumeration Suite v2.0 🔍          
EOF
echo -e "${NC}"

if [ -z "$1" ]; then
    echo -e "${BRIGHT_RED}[!] Usage: $0 <domain> [options]${NC}"
    echo -e "${YELLOW}    Options:${NC}"
    echo -e "${SILVER}    -a, --all       Run all enumeration methods${NC}"
    echo -e "${SILVER}    -p, --passive   Run only passive methods${NC}"
    echo -e "${SILVER}    -b, --brute     Run brute force methods${NC}"
    echo -e "${SILVER}    -r, --resolve   Resolve found subdomains${NC}"
    echo -e "${SILVER}    -h, --http      HTTP probe discovered hosts${NC}"
    exit 1
fi

DOMAIN=$1
MODE=${2:-"all"}
OUTPUT_DIR="subdomain_enum_${DOMAIN}_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo -e "${GOLD}[+] Target Domain: ${BRIGHT_CYAN}${DOMAIN}${NC}"
echo -e "${GOLD}[+] Output Directory: ${BRIGHT_CYAN}${OUTPUT_DIR}${NC}"
echo -e "${GOLD}[+] Mode: ${BRIGHT_CYAN}${MODE}${NC}"
echo ""

TOTAL_STEPS=0
CURRENT_STEP=0

print_progress() {
    local msg="$1"
    local color="$2"
    CURRENT_STEP=$((CURRENT_STEP + 1))
    echo -e "${color}[${CURRENT_STEP}/${TOTAL_STEPS}] ${msg}${NC}"
}

print_success() {
    echo -e "${BRIGHT_GREEN}[✓] $1${NC}"
}

print_error() {
    echo -e "${BRIGHT_RED}[✗] $1${NC}"
}

print_info() {
    echo -e "${BRIGHT_BLUE}[ℹ] $1${NC}"
}

print_warning() {
    echo -e "${ORANGE}[⚠] $1${NC}"
}

check_deps() {
    print_info "Checking dependencies..."
    local deps=("curl" "jq" "grep" "sed" "sort" "tee")
    local optional_deps=("subfinder" "sublist3r" "findomain" "assetfinder" "shuffledns" "httpx" "dnsx" "anew" "csprecon" "github-subdomains" "prips")

    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            print_error "Required dependency missing: $dep"
            exit 1
        fi
    done

    for dep in "${optional_deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            print_warning "Optional tool not found: $dep"
        fi
    done
}

passive_enum() {
    echo -e "${PURPLE}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║           🔍 PASSIVE ENUMERATION PHASE                     ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    print_progress "Querying DNSDumpster API..." "$CYAN"
    curl -s -H "X-API-Key: d305dbd3efdfbb2623b09cb3818f3c33f294c1be0516728c8f322b524ee1e2e1" \
        "https://api.dnsdumpster.com/domain/${DOMAIN}" 2>/dev/null | \
        jq -r '.subdomains[]? // empty' 2>/dev/null | \
        tee -a "${OUTPUT_DIR}/dnsdumpster.txt" > /dev/null && \
        print_success "DNSDumpster completed" || print_error "DNSDumpster failed"
    
    print_progress "Scraping RapidDNS..." "$TEAL"
    curl -s "https://rapiddns.io/subdomain/${DOMAIN}?full=1" 2>/dev/null | \
        grep -oP '(?<=target="_blank">)[^<]+' | \
        grep "${DOMAIN}" | \
        tee -a "${OUTPUT_DIR}/rapiddns.txt" > /dev/null && \
        print_success "RapidDNS completed" || print_error "RapidDNS failed"
    
    print_progress "Querying HackerTarget..." "$LIME"
    curl -s "https://api.hackertarget.com/hostsearch/?q=${DOMAIN}" 2>/dev/null | \
        cut -d',' -f1 | \
        tee -a "${OUTPUT_DIR}/hackertarget.txt" > /dev/null && \
        print_success "HackerTarget completed" || print_error "HackerTarget failed"
    
    print_progress "Querying AlienVault OTX..." "$MAGENTA"
    curl -s "https://otx.alienvault.com/api/v1/indicators/domain/${DOMAIN}/passive_dns" 2>/dev/null | \
        jq -r '.passive_dns[]?.hostname // empty' 2>/dev/null | \
        sort -u | \
        tee -a "${OUTPUT_DIR}/alienvault.txt" > /dev/null && \
        print_success "AlienVault OTX completed" || print_error "AlienVault OTX failed"
    
    print_progress "Querying URLScan.io..." "$PINK"
    curl -s "https://urlscan.io/api/v1/search/?q=domain:${DOMAIN}" 2>/dev/null | \
        jq -r '.results[]?.page.domain // empty' 2>/dev/null | \
        sort -u | grep "${DOMAIN}" | \
        tee -a "${OUTPUT_DIR}/urlscan.txt" > /dev/null && \
        print_success "URLScan.io completed" || print_error "URLScan.io failed"
    
    print_progress "Querying Wayback Machine..." "$ORANGE"
    curl -s "http://web.archive.org/cdx/search/cdx?url=*.${DOMAIN}/*&output=text&fl=original&collapse=urlkey" 2>/dev/null | \
        sed -e 's_https*://__' -e 's/\/.*//g' | \
        sort -u | \
        tee -a "${OUTPUT_DIR}/wayback.txt" > /dev/null && \
        print_success "Wayback Machine completed" || print_error "Wayback Machine failed"
    
    print_progress "Querying CommonCrawl..." "$GOLD"
    curl -s "https://index.commoncrawl.org/CC-MAIN-2023-50-index?url=*.${DOMAIN}&output=json" 2>/dev/null | \
        jq -r '.url // empty' 2>/dev/null | \
        sed -e 's_https*://__' -e 's/\/.*//g' | \
        sort -u | \
        tee -a "${OUTPUT_DIR}/commoncrawl.txt" > /dev/null && \
        print_success "CommonCrawl completed" || print_error "CommonCrawl failed"
    
    if [ -n "${SECURITYTRAILS_API_KEY}" ]; then
        print_progress "Querying SecurityTrails..." "$SILVER"
        curl -s "https://api.securitytrails.com/v1/domain/${DOMAIN}/subdomains" \
            -H "APIKEY: ${SECURITYTRAILS_API_KEY}" 2>/dev/null | \
            jq -r '.subdomains[]? // empty' 2>/dev/null | \
            sed "s/$/.${DOMAIN}/" | \
            tee -a "${OUTPUT_DIR}/securitytrails.txt" > /dev/null && \
            print_success "SecurityTrails completed" || print_error "SecurityTrails failed"
    fi
    
    if command -v github-subdomains &> /dev/null; then
        print_progress "Searching GitHub for subdomains..." "$WHITE"
        github-subdomains -d "${DOMAIN}" -t "${GITHUB_TOKEN}" 2>/dev/null | \
            tee -a "${OUTPUT_DIR}/github.txt" > /dev/null && \
            print_success "GitHub search completed" || print_error "GitHub search failed"
    fi
}

tool_enum() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║           🛠️  TOOL-BASED ENUMERATION PHASE                 ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    if command -v subfinder &> /dev/null; then
        print_progress "Running Subfinder..." "$CYAN"
        subfinder -d "${DOMAIN}" -silent 2>/dev/null | \
            tee -a "${OUTPUT_DIR}/subfinder.txt" > /dev/null && \
            print_success "Subfinder completed" || print_error "Subfinder failed"
    fi
    
    if command -v findomain &> /dev/null; then
        print_progress "Running Findomain..." "$LIME"
        findomain -t "${DOMAIN}" -u "${OUTPUT_DIR}/findomain.txt" 2>/dev/null && \
            print_success "Findomain completed" || print_error "Findomain failed"
    fi
    
    if command -v assetfinder &> /dev/null; then
        print_progress "Running Assetfinder..." "$MAGENTA"
        assetfinder "${DOMAIN}" | grep "${DOMAIN}" 2>/dev/null | \
            tee -a "${OUTPUT_DIR}/assetfinder.txt" > /dev/null && \
            print_success "Assetfinder completed" || print_error "Assetfinder failed"
    fi
    
    if command -v csprecon &> /dev/null; then
        print_progress "Running CSPRecon..." "$PINK"
        csprecon -u "https://${DOMAIN}" -o "${OUTPUT_DIR}/csprecon.txt" 2>/dev/null && \
            print_success "CSPRecon completed" || print_error "CSPRecon failed"
    fi
    
    if command -v subdog &> /dev/null; then
        print_progress "Running Subdog..." "$ORANGE"
        echo "${DOMAIN}" | subdog 2>/dev/null | \
            tee -a "${OUTPUT_DIR}/subdog.txt" > /dev/null && \
            print_success "Subdog completed" || print_error "Subdog failed"
    fi
}

brute_enum() {
    echo -e "${RED}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║           ⚡ BRUTE FORCE ENUMERATION PHASE                  ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    WORDLIST="${WORDLIST:-/usr/share/wordlists/dnsrecon/subdomains-top1mil-5000.txt}"
    if [ ! -f "$WORDLIST" ]; then
        print_warning "Wordlist not found at $WORDLIST, using default..."
        WORDLIST="wordlist.txt"
    fi
    
    RESOLVERS="${RESOLVERS:-resolvers.txt}"
    if [ ! -f "$RESOLVERS" ]; then
        print_warning "Resolvers file not found, creating default..."
        echo -e "8.8.8.8\n1.1.1.1\n9.9.9.9" > "$RESOLVERS"
    fi
    
    if command -v shuffledns &> /dev/null; then
        print_progress "Running ShuffleDNS brute force..." "$BRIGHT_RED"
        shuffledns -d "${DOMAIN}" -w "$WORDLIST" -r "$RESOLVERS" -mode bruteforce -silent 2>/dev/null | \
            tee -a "${OUTPUT_DIR}/shuffledns_brute.txt" > /dev/null && \
            print_success "ShuffleDNS brute force completed" || print_error "ShuffleDNS brute force failed"
    fi
    
    if command -v subfinder &> /dev/null; then
        print_progress "Running Subfinder with wordlist..." "$BRIGHT_BLUE"
        subfinder -d "${DOMAIN}" -all 2>/dev/null | \
            tee -a "${OUTPUT_DIR}/subfinder_all.txt" > /dev/null && \
            print_success "Subfinder (all sources) completed" || print_error "Subfinder failed"
    fi
}

main() {
    check_deps
    
    case "$MODE" in
        -p|--passive)
            TOTAL_STEPS=9
            passive_enum
            ;;
        -b|--brute)
            TOTAL_STEPS=2
            brute_enum
            ;;
        -t|--tools)
            TOTAL_STEPS=5
            tool_enum
            ;;
        -a|--all|*)
            TOTAL_STEPS=16
            passive_enum
            tool_enum
            brute_enum
            ;;
    esac
}

main

```
