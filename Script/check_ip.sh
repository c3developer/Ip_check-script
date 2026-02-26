#!/bin/bash

# =============================================
# Скрипт для проверки доступности IP-адреса
# Режимы: ping (сводка), порты, оба, ping в реальном времени
# Адаптирован для Git Bash (Windows)
# =============================================

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Список портов для проверки (можно изменить)
PORTS=(22 80 443 21 25 3389 3306 5432)

# Функция паузы
pause() {
    echo ""
    read -p "Нажмите Enter для продолжения..."
}

# Определяем, работаем ли мы в окружении Windows (Git Bash / MSYS)
is_windows() {
    if command -v cmd.exe &> /dev/null; then
        return 0
    fi
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        return 0
    fi
    return 1
}

# Функция получения статистики ping (Windows-версия, краткий опрос)
get_ping_stats_windows() {
    local ip=$1
    local ping_output
    local trans recv loss rtt_min rtt_avg rtt_max

    ping_output=$(cmd.exe /c "ping -n 4 -w 1000 $ip" 2>&1)

    # Парсим отправленные/полученные/потери
    if [[ $ping_output =~ ([0-9]+)[^0-9]+([0-9]+)[^0-9]+([0-9]+)[^0-9]+([0-9]+)% ]]; then
        trans="${BASH_REMATCH[1]}"
        recv="${BASH_REMATCH[2]}"
        loss="${BASH_REMATCH[4]}"
    else
        if [[ $ping_output =~ отправлено[^0-9]*([0-9]+) ]]; then trans="${BASH_REMATCH[1]}"; else trans="—"; fi
        if [[ $ping_output =~ получено[^0-9]*([0-9]+) ]]; then recv="${BASH_REMATCH[1]}"; else recv="—"; fi
        if [[ $ping_output =~ потерь[^0-9]*([0-9]+)% ]]; then loss="${BASH_REMATCH[1]}"; else loss="—"; fi
        if [[ $ping_output =~ Sent[^0-9]*([0-9]+) ]]; then trans="${BASH_REMATCH[1]}"; fi
        if [[ $ping_output =~ Received[^0-9]*([0-9]+) ]]; then recv="${BASH_REMATCH[1]}"; fi
        if [[ $ping_output =~ loss[^0-9]*([0-9]+)% ]]; then loss="${BASH_REMATCH[1]}"; fi
    fi

    # Парсим RTT
    if [[ $ping_output =~ минимальное[^0-9]*([0-9]+)ms[^0-9]+максимальное[^0-9]*([0-9]+)ms[^0-9]+среднее[^0-9]*([0-9]+)ms ]]; then
        rtt_min="${BASH_REMATCH[1]}"
        rtt_max="${BASH_REMATCH[2]}"
        rtt_avg="${BASH_REMATCH[3]}"
    elif [[ $ping_output =~ Minimum[^0-9]*([0-9]+)ms[^0-9]+Maximum[^0-9]*([0-9]+)ms[^0-9]+Average[^0-9]*([0-9]+)ms ]]; then
        rtt_min="${BASH_REMATCH[1]}"
        rtt_max="${BASH_REMATCH[2]}"
        rtt_avg="${BASH_REMATCH[3]}"
    else
        rtt_min="—"
        rtt_avg="—"
        rtt_max="—"
    fi

    if [[ "$recv" != "—" && "$recv" -gt 0 ]]; then
        ping_status_text="доступен"
        ping_status="${GREEN}доступен${NC}"
    else
        ping_status_text="недоступен"
        ping_status="${RED}недоступен${NC}"
    fi

    packet_str="$trans/$recv/$loss%"
    rtt_str="$rtt_min/$rtt_avg/$rtt_max"
}

# Функция получения статистики ping (Unix-версия, краткий опрос)
get_ping_stats_unix() {
    local ip=$1
    local ping_output
    local trans recv loss rtt_min rtt_avg rtt_max

    ping_output=$(ping -c 4 -W 1 "$ip" 2>&1)

    if [ $? -eq 0 ]; then
        ping_status_text="доступен"
        ping_status="${GREEN}доступен${NC}"
    else
        ping_status_text="недоступен"
        ping_status="${RED}недоступен${NC}"
    fi

    if [[ $ping_output =~ ([0-9]+)[[:space:]]+packets?[[:space:]]+transmitted || $ping_output =~ ([0-9]+)[[:space:]]+пакетов?[[:space:]]+отправлено ]]; then
        trans="${BASH_REMATCH[1]}"
    else
        trans="—"
    fi

    if [[ $ping_output =~ ([0-9]+)[[:space:]]+received || $ping_output =~ ([0-9]+)[[:space:]]+получено ]]; then
        recv="${BASH_REMATCH[1]}"
    else
        recv="—"
    fi

    if [[ $ping_output =~ ([0-9]+)%[[:space:]]+packet[[:space:]]+loss || $ping_output =~ ([0-9]+)%[[:space:]]+потерь ]]; then
        loss="${BASH_REMATCH[1]}"
    else
        loss="—"
    fi

    if [[ $ping_output =~ rtt[[:space:]]+min/avg/max/mdev[[:space:]]*=[[:space:]]*([0-9.]+)/([0-9.]+)/([0-9.]+) ]]; then
        rtt_min="${BASH_REMATCH[1]}"
        rtt_avg="${BASH_REMATCH[2]}"
        rtt_max="${BASH_REMATCH[3]}"
    elif [[ $ping_output =~ rtt[[:space:]]+мин/ср/макс/mdev[[:space:]]*=[[:space:]]*([0-9.]+)/([09.]+)/([0-9.]+) ]]; then
        rtt_min="${BASH_REMATCH[1]}"
        rtt_avg="${BASH_REMATCH[2]}"
        rtt_max="${BASH_REMATCH[3]}"
    else
        rtt_min="—"
        rtt_avg="—"
        rtt_max="—"
    fi

    packet_str="$trans/$recv/$loss%"
    rtt_str="$rtt_min/$rtt_avg/$rtt_max"
}

# Выбираем подходящую функцию ping для краткого опроса
if is_windows; then
    get_ping_stats() { get_ping_stats_windows "$1"; }
else
    get_ping_stats() { get_ping_stats_unix "$1"; }
fi

# Функция для запуска ping в реальном времени
realtime_ping() {
    local ip=$1
    echo -e "${CYAN}Запуск ping в реальном времени к $ip${NC}"
    echo -e "${YELLOW}Для остановки нажмите Ctrl+C${NC}"
    echo "----------------------------------------"
    if is_windows; then
        # Windows: непрерывный ping через cmd
        cmd.exe /c "ping -t $ip"
    else
        # Linux/Unix: непрерывный ping (обычно без -c)
        ping "$ip"
    fi
    # После завершения ping (по Ctrl+C) вернёмся сюда
    echo ""
    echo -e "${GREEN}Пинг остановлен.${NC}"
}

# Определение доступного метода проверки портов
detect_port_check_method() {
    if (timeout 1 bash -c "echo >/dev/tcp/8.8.8.8/53" 2>/dev/null); then
        echo "devtcp"
        return
    fi
    if command -v nc &> /dev/null; then
        if nc -z -w1 8.8.8.8 53 2>/dev/null; then
            echo "nc"
            return
        fi
    fi
    if command -v powershell.exe &> /dev/null; then
        echo "powershell"
        return
    fi
    echo "none"
}

# Функция проверки порта выбранным методом
check_port() {
    local ip=$1
    local port=$2
    local method=$3
    case $method in
        devtcp)
            timeout 1 bash -c "echo >/dev/tcp/$ip/$port" 2>/dev/null && echo "открыт" || echo "закрыт"
            ;;
        nc)
            nc -z -w1 "$ip" "$port" 2>/dev/null && echo "открыт" || echo "закрыт"
            ;;
        powershell)
            powershell.exe -Command "\$tcp = New-Object System.Net.Sockets.TcpClient; \$conn = \$tcp.BeginConnect('$ip',$port,\$null,\$null); \$wait = \$conn.AsyncWaitHandle.WaitOne(1000); if(\$wait -and \$tcp.Connected) { exit 0 } else { exit 1 }" >/dev/null 2>&1
            if [ $? -eq 0 ]; then echo "открыт"; else echo "закрыт"; fi
            ;;
        *)
            echo "закрыт"
            ;;
    esac
}

# Функция сканирования портов с индикатором прогресса
check_ports_with_progress() {
    local ip=$1
    local method=$2
    local total=${#PORTS[@]}
    local current=0
    local port
    local result
    open_ports_result=""

    for port in "${PORTS[@]}"; do
        current=$((current + 1))
        percent=$((current * 100 / total))
        printf "\rСканирование портов: %d/%d (%d%%)" "$current" "$total" "$percent"
        result=$(check_port "$ip" "$port" "$method")
        if [ "$result" == "открыт" ]; then
            open_ports_result+="$port "
        fi
    done
    printf "\n"
}

# Главное меню
while true; do
    echo -e "${YELLOW}========================================${NC}"
    echo -e "${YELLOW}  Проверка доступности IP-адреса${NC}"
    echo -e "${YELLOW}========================================${NC}"
    echo ""

    read -p "Введите IP-адрес или домен для проверки (или 'q' для выхода): " raw_input
    if [[ "$raw_input" == "q" || "$raw_input" == "Q" ]]; then
        exit 0
    fi
    target_ip="$(echo -e "${raw_input}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

    if [ -z "$target_ip" ]; then
        echo -e "${RED}IP не введён.${NC}"
        continue
    fi

    echo ""
    echo -e "${YELLOW}Выберите тип проверки:${NC}"
    echo "1 - Только ping (краткая сводка)"
    echo "2 - Только сканирование портов (TCP)"
    echo "3 - И ping (сводка), и порты"
    echo "4 - Ping в реальном времени (нажмите Ctrl+C для остановки)"
    read -p "Ваш выбор (1-4): " choice

    if [[ ! "$choice" =~ ^[1-4]$ ]]; then
        echo -e "${RED}Неверный выбор.${NC}"
        continue
    fi

    # Если выбран режим 4 (ping в реальном времени)
    if [ "$choice" == "4" ]; then
        realtime_ping "$target_ip"
        pause
        continue
    fi

    # Для режимов 1-3 продолжаем как раньше
    port_method="none"
    if [[ "$choice" == "2" || "$choice" == "3" ]]; then
        echo ""
        echo -e "${YELLOW}Определение метода проверки портов...${NC}"
        port_method=$(detect_port_check_method)
        if [ "$port_method" == "none" ]; then
            echo -e "${RED}Не найден ни один метод проверки портов. Будут показаны только результаты ping.${NC}"
        else
            echo -e "${GREEN}Используется метод: $port_method${NC}"
        fi
    fi

    echo ""
    echo -e "${GREEN}Выполняется проверка...${NC}"

    # Переменные для результатов
    ping_status="—"
    ping_status_text="—"
    packet_str="—"
    rtt_str="—"
    open_ports="—"

    # --- Ping (сводка) ---
    if [[ "$choice" == "1" || "$choice" == "3" ]]; then
        echo -n "Выполнение ping... "
        get_ping_stats "$target_ip"
        echo -e "${GREEN}OK${NC}"
    fi

    # --- Порты ---
    if [[ "$choice" == "2" || "$choice" == "3" ]]; then
        if [ "$port_method" != "none" ]; then
            check_ports_with_progress "$target_ip" "$port_method"
            open_ports="$open_ports_result"
            if [ -z "$open_ports" ]; then
                open_ports="—"
            fi
        else
            echo "Сканирование портов пропущено (нет метода)."
        fi
    fi

    # --- Вывод таблицы ---
    echo ""
    echo -e "${GREEN}Результаты проверки:${NC}"
    printf "\n%-15s %-15s %-25s %-20s %-20s\n" "IP-адрес" "Статус ping" "Пакеты (посл/пол/пот%)" "RTT мин/ср/макс(ms)" "Открытые порты"
    printf "%0.s-" {1..100}
    printf "\n"

    printf "%-15s " "$target_ip"
    if [ "$ping_status" != "—" ]; then
        echo -en "$ping_status"
    else
        echo -n "—"
    fi
    printf " %-25s %-20s %-20s\n" "$packet_str" "$rtt_str" "$open_ports"

    printf "%0.s-" {1..100}
    printf "\n"

    if [[ "$ping_status_text" == "недоступен" && "$choice" == "3" && "$open_ports" != "—" ]]; then
        echo -e "${YELLOW}Примечание: ping может быть заблокирован файрволом, но порты открыты. Сервер работает.${NC}"
    fi

    pause
done