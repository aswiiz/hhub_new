document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navContainer = document.querySelector('.nav-container');

    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            navContainer.classList.toggle('active');
        });
    }

    // --- DIARY (DAILY HEALTH LOG) ---
    const logForm = document.getElementById('health-log-form');
    const logTableBody = document.getElementById('log-table-body');
    const dateInput = document.getElementById('date');
    const smokingToggle = document.getElementById('smoking');
    const smokingLabel = document.getElementById('smoking-label');
    const heightGroup = document.getElementById('height-group');
    const heightInput = document.getElementById('height');
    const successBanner = document.getElementById('success-banner');

    if (dateInput) {
        // Auto-fill today's date
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
    }

    if (smokingToggle) {
        smokingToggle.addEventListener('change', () => {
            smokingLabel.innerText = smokingToggle.checked ? 'Yes' : 'No';
        });
    }

    // Check if height exists
    async function checkHeight() {
        if (!heightGroup) return;
        try {
            const resp = await fetch('/api/height');
            const data = await resp.json();
            if (data.height) {
                heightGroup.style.display = 'none';
                heightInput.removeAttribute('required');
                heightInput.value = data.height;
            }
        } catch (e) {
            console.error(e);
        }
    }

    async function loadLogs() {
        if (!logTableBody) return;
        try {
            const response = await fetch('/api/diary');
            const logs = await response.json();

            if (logs.length === 0) {
                logTableBody.innerHTML = '<tr><td colspan="9" class="text-center">No logs found.</td></tr>';
                return;
            }

            logTableBody.innerHTML = logs.map(log => `
                <tr>
                    <td>${log.date}</td>
                    <td>${log.sleep_hours}h</td>
                    <td>${log.steps}</td>
                    <td>${log.exercise_mins}m</td>
                    <td>${log.water_liters}L</td>
                    <td>Level ${log.junk_food}</td>
                    <td>${log.smoking}</td>
                    <td>${log.alcohol_units}u</td>
                    <td>${log.weight_kg}kg</td>
                </tr>
            `).join('');
        } catch (e) {
            console.error(e);
        }
    }

    if (logForm) {
        checkHeight();
        loadLogs();

        logForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Validation
            let isValid = true;
            const fields = [
                'date', 'sleep_hours', 'steps', 'exercise_mins',
                'water_liters', 'junk_food', 'alcohol_units', 'weight'
            ];

            if (heightGroup.style.display !== 'none') {
                fields.push('height');
            }

            fields.forEach(f => {
                const input = document.getElementById(f);
                const err = document.getElementById(`err-${f}`);
                if (!input.value) {
                    err.style.display = 'block';
                    isValid = false;
                } else {
                    err.style.display = 'none';
                }
            });

            if (!isValid) return;

            const payload = {
                date: document.getElementById('date').value,
                sleep_hours: document.getElementById('sleep_hours').value,
                steps: document.getElementById('steps').value,
                exercise_mins: document.getElementById('exercise_mins').value,
                water_liters: document.getElementById('water_liters').value,
                junk_food: document.getElementById('junk_food').value,
                smoking: document.getElementById('smoking').checked,
                alcohol_units: document.getElementById('alcohol_units').value,
                weight: document.getElementById('weight').value,
                height: document.getElementById('height').value
            };

            try {
                const response = await fetch('/api/diary', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    successBanner.style.display = 'block';
                    setTimeout(() => { successBanner.style.display = 'none'; }, 3000);
                    logForm.reset();
                    dateInput.value = new Date().toISOString().split('T')[0];
                    checkHeight();
                    loadLogs();
                }
            } catch (err) {
                console.error(err);
            }
        });
    }

    // --- ANALYZE (DATA-DRIVEN) ---
    const runAnalysisBtn = document.getElementById('run-analysis-btn');
    const analyzeInitial = document.getElementById('analyze-initial');
    const analyzeLoading = document.getElementById('analyze-loading');
    const analyzeError = document.getElementById('analyze-error');
    const analyzeResult = document.getElementById('analyze-result');
    const resultStatus = document.getElementById('result-status');
    const resultMessage = document.getElementById('result-message');
    const resultIcon = document.getElementById('result-icon');
    const metricsSummary = document.getElementById('metrics-summary');
    const errorMessage = document.getElementById('error-message');
    const daysCount = document.getElementById('days-count');
    const healthBadge = document.getElementById('health-badge');
    const recList = document.getElementById('recommendations-list');

    if (runAnalysisBtn) {
        runAnalysisBtn.addEventListener('click', async () => {
            analyzeInitial.style.display = 'none';
            analyzeLoading.style.display = 'block';

            try {
                // 1. Fetch all records
                const response = await fetch('/api/diary');
                const logs = await response.json();

                // 2. Check minimum data requirement
                if (logs.length < 3) {
                    analyzeLoading.style.display = 'none';
                    analyzeError.style.display = 'block';
                    errorMessage.innerText = "Minimum 3 days of data required for analysis.";
                    return;
                }

                // 3. Take latest complete set of 3 logs (skipping newest if not a full set of 3)
                const skip = logs.length % 3;
                const recentLogs = logs.slice(skip, skip + 3);
                const count = recentLogs.length;

                console.log(`Analyzing set of 3 (skipped ${skip} newest logs out of ${logs.length})`);


                // 4. Calculate averages
                const averages = recentLogs.reduce((acc, log) => {
                    acc.sleep += parseFloat(log.sleep_hours || 0);
                    acc.steps += parseInt(log.steps || 0);
                    acc.exercise += parseInt(log.exercise_mins || 0);
                    acc.water += parseFloat(log.water_liters || 0);
                    acc.junk += parseInt(log.junk_food || 0);
                    acc.alcohol += parseInt(log.alcohol_units || 0);
                    if (log.smoking === 'Yes') acc.smokingCount++;
                    return acc;
                }, { sleep: 0, steps: 0, exercise: 0, water: 0, junk: 0, alcohol: 0, smokingCount: 0 });

                const processedData = {
                    avg_sleep: averages.sleep / count,
                    avg_steps: averages.steps / count,
                    avg_exercise: averages.exercise / count,
                    avg_water: averages.water / count,
                    avg_junk: averages.junk / count,
                    avg_alcohol: averages.alcohol / count,
                    smoking_freq: averages.smokingCount / count,
                    weight: parseFloat(recentLogs[0].weight_kg), // Latest weight
                    height: parseFloat(recentLogs[0].height_cm)  // Stored height
                };

                // 5. BMI Calculation
                if (processedData.height && processedData.weight) {
                    const heightInMeters = processedData.height / 100;
                    processedData.bmi = processedData.weight / (heightInMeters * heightInMeters);
                }

                // 6. Call backend predict
                const predictResp = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(processedData)
                });
                const prediction = await predictResp.json();

                // 7. Display Results
                analyzeLoading.style.display = 'none';
                analyzeResult.style.display = 'block';

                const skippedInfo = document.getElementById('skipped-info');

                if (daysCount) daysCount.innerText = count;
                if (skippedInfo) {
                    skippedInfo.innerText = skip > 0 ? `(Skipped ${skip} newest logs to form a set of 3)` : '';
                }

                if (healthBadge) healthBadge.innerText = prediction.chance;

                if (healthBadge) healthBadge.className = 'health-badge'; // Reset
                let recommendations = prediction.recommendations || [];

                if (healthBadge) {
                    if (prediction.chance === 'Low Chance') {
                        healthBadge.classList.add('badge-low');
                    } else if (prediction.chance === 'Moderate Chance') {
                        healthBadge.classList.add('badge-moderate');
                    } else {
                        healthBadge.classList.add('badge-high');
                    }
                }

                if (recList) recList.innerHTML = recommendations.map(rec => `<li>${rec}</li>`).join('');

                // Display metrics summary
                metricsSummary.innerHTML = `
                    <div class="metric-item">Avg Sleep: <span>${processedData.avg_sleep.toFixed(1)}h</span></div>
                    <div class="metric-item">Avg Steps: <span>${Math.round(processedData.avg_steps)}</span></div>
                    <div class="metric-item">BMI: <span>${processedData.bmi ? processedData.bmi.toFixed(1) : 'N/A'}</span></div>
                `;

            } catch (err) {
                console.error(err);
                analyzeLoading.style.display = 'none';
                analyzeError.style.display = 'block';
                errorMessage.innerText = "An error occurred during analysis.";
            }
        });
    }

    // --- LOADER ---
    const loaderWrapper = document.getElementById('loader-wrapper');
    if (loaderWrapper) {
        // Set timeout for 10 seconds (10000ms)
        setTimeout(() => {
            loaderWrapper.classList.add('fade-out');
            // Remove from DOM after transition completes (0.8s)
            setTimeout(() => {
                loaderWrapper.style.display = 'none';
            }, 800);
        }, 10000);
    }
});

