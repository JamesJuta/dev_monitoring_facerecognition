@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('home'))