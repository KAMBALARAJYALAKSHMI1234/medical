// API URLs
const API_URLS = {
    subscription: 'http://localhost:8000/api/subscriptions/',
    invoice: 'http://localhost:8004/api/invoices/',
    doctor: 'http://localhost:8001/api/doctors/',
    plan: 'http://localhost:8002/api/plans/',
    coupon: 'http://localhost:8003/api/coupons/',
    agent: 'http://localhost:8005/api/agents/'
};

let currentPlanPrice = 0;
let currentCouponPercentage = 0;
let couponData = {};

// Debug function to see API responses
async function debugAPI(url, name) {
    try {
        console.log(`🔍 Debug ${name}: ${url}`);
        const response = await fetch(url);
        const data = await response.json();
        console.log(`📊 ${name} Response:`, data);
        return { success: true, data: data };
    } catch (error) {
        console.log(`❌ ${name} Error:`, error);
        return { success: false, error: error.message };
    }
}

// Generate automatic invoice number
function generateInvoiceNumber() {
    const timestamp = new Date().getTime();
    const random = Math.floor(Math.random() * 1000);
    return `INV-${timestamp}-${random}`;
}

// Check service status
async function checkServiceStatus() {
    const statusDiv = document.getElementById('serviceStatus');
    statusDiv.innerHTML = '';

    for (const [service, url] of Object.entries(API_URLS)) {
        try {
            const response = await fetch(url);
            const status = response.ok ? '🟢 Online' : '🔴 Offline';
            const statusElement = document.createElement('span');
            statusElement.className = `service-status ${response.ok ? 'service-online' : 'service-offline'}`;
            statusElement.textContent = `${service}: ${status}`;
            statusDiv.appendChild(statusElement);
        } catch (error) {
            const statusElement = document.createElement('span');
            statusElement.className = 'service-status service-offline';
            statusElement.textContent = `${service}: 🔴 Offline`;
            statusDiv.appendChild(statusElement);
        }
    }
}

// Extract array from API response (handles both arrays and objects)
function extractDataArray(responseData) {
    console.log('📦 Raw response data:', responseData);
    
    // If it's already an array, return it
    if (Array.isArray(responseData)) {
        return responseData;
    }
    
    // If it's an object, look for common array property names
    if (typeof responseData === 'object' && responseData !== null) {
        // Try common property names that might contain the array
        const possibleArrayProps = [
            'data', 'results', 'items', 'doctors', 'plans', 
            'coupons', 'agents', 'invoices', 'subscriptions'
        ];
        
        for (const prop of possibleArrayProps) {
            if (Array.isArray(responseData[prop])) {
                console.log(`✅ Found array in property: ${prop}`);
                return responseData[prop];
            }
        }
        
        // If no array property found, check if object has numeric keys (like {0: {}, 1: {}})
        const keys = Object.keys(responseData);
        const numericKeys = keys.filter(key => !isNaN(key));
        if (numericKeys.length > 0) {
            console.log('✅ Found numeric keys, converting to array');
            return numericKeys.map(key => responseData[key]);
        }
        
        // If it's a single object, wrap it in array
        if (responseData.doctor_id || responseData.plan_id) {
            console.log('✅ Single object found, wrapping in array');
            return [responseData];
        }
    }
    
    console.log('❌ Could not extract array from response');
    return [];
}

// Load dropdown data with object/array handling
async function loadDropdownData() {
    console.log('🔄 Loading dropdown data...');
    
    try {
        // Load doctors with object handling
        const doctorsResult = await debugAPI(API_URLS.doctor, 'Doctors');
        const doctors = extractDataArray(doctorsResult.data);
        const doctorSelect = document.getElementById('doctorSelect');
        doctorSelect.innerHTML = '<option value="">Select Doctor</option>';
        
        console.log('👨‍⚕️ Processed doctors:', doctors);

        if (Array.isArray(doctors) && doctors.length > 0) {
            doctors.forEach(doctor => {
                const option = document.createElement('option');
                const doctorId = doctor.doctor_id || doctor.id || doctor.DOCTOR_ID;
                const firstName = doctor.doctor_first_name || doctor.first_name || doctor.DOCTOR_FIRST_NAME || 'Unknown';
                const lastName = doctor.doctor_last_name || doctor.last_name || doctor.DOCTOR_LAST_NAME || '';
                
                if (doctorId) {
                    option.value = doctorId;
                    option.textContent = `Dr. ${firstName} ${lastName}`;
                    doctorSelect.appendChild(option);
                }
            });
        } else {
            doctorSelect.innerHTML = '<option value="">No doctors found</option>';
        }

        // Load plans with object handling
        const plansResult = await debugAPI(API_URLS.plan, 'Plans');
        const plans = extractDataArray(plansResult.data);
        const planSelect = document.getElementById('planSelect');
        planSelect.innerHTML = '<option value="">Select Plan</option>';
        
        console.log('📋 Processed plans:', plans);

        if (Array.isArray(plans) && plans.length > 0) {
            plans.forEach(plan => {
                const option = document.createElement('option');
                const planId = plan.plan_id || plan.id || plan.PLAN_ID;
                const planName = plan.plan_name || plan.name || plan.PLAN_NAME || 'Unknown Plan';
                const price = plan.price || plan.PRICE || plan.plan_price || 0;
                
                if (planId) {
                    option.value = planId;
                    option.textContent = `${planName} - $${price}`;
                    option.setAttribute('data-price', price);
                    planSelect.appendChild(option);
                }
            });
        } else {
            planSelect.innerHTML = '<option value="">No plans found</option>';
        }

        // Load coupons (already working)
        const couponsResult = await debugAPI(API_URLS.coupon, 'Coupons');
        const coupons = extractDataArray(couponsResult.data);
        const couponSelect = document.getElementById('couponSelect');
        couponSelect.innerHTML = '<option value="">Select Coupon</option>';
        
        if (Array.isArray(coupons) && coupons.length > 0) {
            coupons.forEach(coupon => {
                const option = document.createElement('option');
                const couponId = coupon.coupon_id || coupon.id || coupon.COUPON_ID;
                const couponName = coupon.coupon_name || coupon.name || coupon.COUPON_NAME || 'Unknown';
                const percentage = coupon.percentage || coupon.PERCENTAGE || coupon.discount_percentage || 0;
                
                if (couponId) {
                    option.value = couponId;
                    option.textContent = `${couponName} - ${percentage}% off`;
                    option.setAttribute('data-percentage', percentage);
                    couponSelect.appendChild(option);
                    
                    couponData[couponId] = percentage;
                }
            });
        } else {
            couponSelect.innerHTML = '<option value="">No coupons found</option>';
        }

        // Load agents (already working)
        const agentsResult = await debugAPI(API_URLS.agent, 'Agents');
        const agents = extractDataArray(agentsResult.data);
        const agentSelect = document.getElementById('agentSelect');
        agentSelect.innerHTML = '<option value="">Select Agent</option>';
        
        if (Array.isArray(agents) && agents.length > 0) {
            agents.forEach(agent => {
                const option = document.createElement('option');
                const agentId = agent.agent_id || agent.id || agent.AGENT_ID;
                const agentName = agent.name || agent.agent_name || agent.NAME || 'Unknown Agent';
                
                if (agentId) {
                    option.value = agentId;
                    option.textContent = agentName;
                    agentSelect.appendChild(option);
                }
            });
        } else {
            agentSelect.innerHTML = '<option value="">No agents found</option>';
        }

        // Set auto-generated invoice number
        document.getElementById('invoiceNumber').value = generateInvoiceNumber();

    } catch (error) {
        console.error('❌ Error loading dropdown data:', error);
        document.getElementById('doctorSelect').innerHTML = '<option value="">Error loading</option>';
        document.getElementById('planSelect').innerHTML = '<option value="">Error loading</option>';
        document.getElementById('couponSelect').innerHTML = '<option value="">Error loading</option>';
        document.getElementById('agentSelect').innerHTML = '<option value="">Error loading</option>';
    }
}

// Update plan price when plan is selected
function updatePlanPrice() {
    const planSelect = document.getElementById('planSelect');
    const selectedOption = planSelect.options[planSelect.selectedIndex];
    
    if (selectedOption && selectedOption.value) {
        currentPlanPrice = parseInt(selectedOption.getAttribute('data-price')) || 0;
        document.getElementById('planPrice').value = currentPlanPrice;
        applyCoupon();
    } else {
        currentPlanPrice = 0;
        document.getElementById('planPrice').value = '';
        document.getElementById('discountAmount').value = '';
        document.getElementById('finalAmount').value = '';
        document.getElementById('priceBreakdown').innerHTML = '';
    }
}

// Apply coupon discount
function applyCoupon() {
    const couponSelect = document.getElementById('couponSelect');
    const selectedOption = couponSelect.options[couponSelect.selectedIndex];
    
    if (selectedOption && selectedOption.value && currentPlanPrice > 0) {
        currentCouponPercentage = parseInt(selectedOption.getAttribute('data-percentage')) || 0;
        const discountAmount = (currentPlanPrice * currentCouponPercentage) / 100;
        const finalAmount = currentPlanPrice - discountAmount;
        
        document.getElementById('discountAmount').value = discountAmount.toFixed(2);
        document.getElementById('finalAmount').value = finalAmount.toFixed(2);
        
        document.getElementById('priceBreakdown').innerHTML = `
            Plan: $${currentPlanPrice} - ${currentCouponPercentage}% ($${discountAmount.toFixed(2)}) = $${finalAmount.toFixed(2)}
        `;
    } else {
        document.getElementById('discountAmount').value = '';
        document.getElementById('finalAmount').value = currentPlanPrice || '';
        document.getElementById('priceBreakdown').innerHTML = '';
    }
}

// Create subscription - FIXED VERSION
document.getElementById('subscriptionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Get and convert discount amount to integer (cents)
    const discountAmountInput = document.getElementById('discountAmount').value;
    let discount_amount = 0;
    
    if (discountAmountInput) {
        // Convert decimal to integer (dollars to cents)
        discount_amount = Math.round(parseFloat(discountAmountInput) * 100);
    }
    
    const formData = {
        doctor_id: document.getElementById('doctorSelect').value,
        plan_id: document.getElementById('planSelect').value,
        coupon_id: document.getElementById('couponSelect').value,
        agent_id: document.getElementById('agentSelect').value,
        plan_pricee: document.getElementById('planPrice').value,
        discount_amount: discount_amount, // Use converted integer value
        invoice: document.getElementById('invoiceNumber').value,
        plan_start_date: new Date().toISOString(),
        plan_end_date: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString(),
        is_active: true
    };

    console.log('📤 Sending form data:', formData);

    try {
        const response = await fetch(API_URLS.subscription, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        const resultDiv = document.getElementById('subscriptionResult');
        
        if (response.ok) {
            resultDiv.innerHTML = `
                <div class="alert alert-success">
                    ✅ Subscription created successfully!<br>
                    Subscription ID: ${result.subscription_id}<br>
                    Invoice will be generated automatically.
                </div>
            `;
            document.getElementById('subscriptionForm').reset();
            document.getElementById('invoiceNumber').value = generateInvoiceNumber();
            loadInvoices();
            loadDropdownData();
        } else {
            resultDiv.innerHTML = `
                <div class="alert alert-danger">
                    ❌ Error: ${JSON.stringify(result)}
                </div>
            `;
        }
    } catch (error) {
        document.getElementById('subscriptionResult').innerHTML = `
            <div class="alert alert-danger">
                ❌ Network error: ${error.message}
            </div>
        `;
    }
});

// Load doctors with object handling
async function loadDoctors() {
    const doctorsList = document.getElementById('doctorsList');
    doctorsList.innerHTML = '<div class="loading">Loading doctors...</div>';
    
    try {
        const response = await fetch(API_URLS.doctor);
        const data = await response.json();
        const doctors = extractDataArray(data);
        
        doctorsList.innerHTML = '';
        
        if (Array.isArray(doctors) && doctors.length > 0) {
            doctors.forEach(doctor => {
                const doctorDiv = document.createElement('div');
                doctorDiv.className = 'data-item';
                
                const firstName = doctor.doctor_first_name || doctor.first_name || doctor.DOCTOR_FIRST_NAME || 'Unknown';
                const lastName = doctor.doctor_last_name || doctor.last_name || doctor.DOCTOR_LAST_NAME || '';
                const email = doctor.email || doctor.EMAIL || 'No email';
                const specialization = doctor.specialization || doctor.SPECIALIZATION || 'General';

                doctorDiv.innerHTML = `
                    <strong>Dr. ${firstName} ${lastName}</strong><br>
                    <small>${email} | ${specialization}</small>
                `;
                doctorsList.appendChild(doctorDiv);
            });
        } else {
            doctorsList.innerHTML = '<div class="alert alert-warning">No doctors found</div>';
        }
    } catch (error) {
        doctorsList.innerHTML = `<div class="alert alert-danger">Error loading doctors: ${error.message}</div>`;
    }
}

// Load plans with object handling
async function loadPlans() {
    const plansList = document.getElementById('plansList');
    plansList.innerHTML = '<div class="loading">Loading plans...</div>';
    
    try {
        const response = await fetch(API_URLS.plan);
        const data = await response.json();
        const plans = extractDataArray(data);
        
        plansList.innerHTML = '';
        
        if (Array.isArray(plans) && plans.length > 0) {
            plans.forEach(plan => {
                const planDiv = document.createElement('div');
                planDiv.className = 'data-item';
                
                const planName = plan.plan_name || plan.name || plan.PLAN_NAME || 'Unknown Plan';
                const price = plan.price || plan.PRICE || 0;
                const duration = plan.duration || plan.DURATION || 0;

                planDiv.innerHTML = `
                    <strong>${planName}</strong><br>
                    <small>$${price} | ${duration} days</small>
                `;
                plansList.appendChild(planDiv);
            });
        } else {
            plansList.innerHTML = '<div class="alert alert-warning">No plans found</div>';
        }
    } catch (error) {
        plansList.innerHTML = `<div class="alert alert-danger">Error loading plans: ${error.message}</div>`;
    }
}

// Load invoices
async function loadInvoices() {
    const invoicesList = document.getElementById('invoicesList');
    invoicesList.innerHTML = '<div class="loading">Loading invoices...</div>';
    
    try {
        const response = await fetch(API_URLS.invoice);
        const invoices = await response.json();
        const invoicesArray = extractDataArray(invoices);
        
        invoicesList.innerHTML = '';
        
        if (Array.isArray(invoicesArray) && invoicesArray.length > 0) {
            invoicesArray.forEach(invoice => {
                const invoiceDiv = document.createElement('div');
                invoiceDiv.className = 'data-item';
                invoiceDiv.innerHTML = `
                    <strong>${invoice.invoice_number}</strong><br>
                    <small>$${invoice.final_amount} | Dr. ID: ${invoice.doctor_id}</small><br>
                    <button class="btn btn-sm btn-outline-primary mt-1" onclick="downloadInvoice(${invoice.invoice_id})">
                        Download
                    </button>
                `;
                invoicesList.appendChild(invoiceDiv);
            });
        } else {
            invoicesList.innerHTML = '<div class="alert alert-warning">No invoices found</div>';
        }
    } catch (error) {
        invoicesList.innerHTML = `<div class="alert alert-danger">Error loading invoices: ${error.message}</div>`;
    }
}

// Download invoice
async function downloadInvoice(invoiceId) {
    try {
        const response = await fetch(`${API_URLS.invoice}${invoiceId}/download/`);
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `invoice-${invoiceId}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            alert('Error downloading invoice');
        }
    } catch (error) {
        alert('Error downloading invoice');
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    checkServiceStatus();
    loadDropdownData();
    loadDoctors();
    loadPlans();
    loadInvoices();
}); check