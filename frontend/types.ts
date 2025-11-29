export interface CashflowSummary {
    total_inflow: number;
    total_outflow: number;
    net_balance: number;
}

export interface Insight {
    type: string;
    severity: 'low' | 'medium' | 'high';
    title: string;
    description: string;
    call_to_action: string;
}

export interface InsightsResponse {
    insights: Insight[];
}

export interface ForecastResponse {
    summary: string;
    trend: 'improving' | 'stable' | 'declining';
    recommendations: string[];
}

export interface SendReminderRequest {
    business_id: number;
    customer_name: string;
    customer_phone: string;
    invoice_number: string;
    amount_due: number;
    due_date: string;
    days_overdue: number;
    preferred_tone: string;
    preferred_language: string;
}

export interface ReminderResponse {
    message: string;
    delivery: {
        status: 'mock' | 'sent' | 'error';
        to: string;
        body: string;
        sid?: string;
        error?: string;
    };
}

export interface PitchdeckRequest {
    business_id: number;
}

export interface Slide {
    heading: string;
    bullets: string[];
}

export interface PitchdeckResponse {
    title: string;
    slides: Slide[];
}
