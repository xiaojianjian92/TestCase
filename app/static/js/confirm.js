
function openProjectDeleteModal(projectId, projectName) {
    const deleteMessage = document.getElementById('deleteMessage');
    const deleteForm = document.getElementById('deleteForm');
    const deleteModal = document.getElementById('deleteModal');

    deleteMessage.textContent = `确定要删除 [${projectName}] 项目及其所有测试用例吗？此操作不可撤销。`;
    deleteForm.action = `/project/${projectId}/delete`;

    deleteModal.classList.remove('hidden');
}

function openTestCaseDeleteModal(testcaseId, testcaseTitle) {
    const deleteMessage = document.getElementById('deleteMessage');
    const deleteForm = document.getElementById('deleteForm');
    const deleteModal = document.getElementById('deleteModal');

    deleteMessage.textContent = `确定要删除 [${testcaseTitle}] 测试用例吗？此操作不可撤销。`;
    deleteForm.action = `/testcases/${testcaseId}/delete`;

    deleteModal.classList.remove('hidden');
}

function closeDeleteModal() {
    const deleteModal = document.getElementById('deleteModal');
    deleteModal.classList.add('hidden');
}
