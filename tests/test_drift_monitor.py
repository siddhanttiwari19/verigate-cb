from app.drift_monitor import DriftMonitor


def test_no_drift_flag_before_window_fills():
    monitor = DriftMonitor(baseline_mean=0.5, baseline_std=0.1)
    status = monitor.record(0.9)
    assert status.drifted is False


def test_drift_detected_when_live_mean_shifts_far_from_baseline():
    monitor = DriftMonitor(baseline_mean=0.5, baseline_std=0.05)
    monitor.window.extend([0.5] * 49)  # pre-fill window just under capacity
    status = monitor.record(0.5)  # window now full, but still centered at baseline
    assert status.drifted is False

    # Now push the whole window toward a drifted region
    drifted_monitor = DriftMonitor(baseline_mean=0.5, baseline_std=0.05)
    for _ in range(50):
        status = drifted_monitor.record(0.95)
    assert status.drifted is True
