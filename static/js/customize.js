console.log('here')
$(document).on("change", "#upload_files", async function(e) {

  for (let x = 0; x < this.files.length; x++){
    
    let form_data = new FormData();
    form_data.append('file', this.files[x]);
    form_data.append('folderID', 'open_folder');
    await $.ajax({
      'url':'/domain/files.upload_file',
      'type':'POST',
      'data': form_data,
       'contentType': false,
      'processData': false
    }).catch(e=>console.log(e));
  }
});